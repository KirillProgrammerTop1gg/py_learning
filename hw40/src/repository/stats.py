from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from sqlalchemy.orm import selectinload

from src.database.models import Skill, User, Exchange, Review, skill_user_association, ExchangeStatus


async def get_top_skills(db: AsyncSession, limit: int = 10) -> list[dict]:
    """Топ-N навичок за кількістю користувачів."""
    stmt = (
        select(
            Skill.id,
            Skill.title,
            Skill.category,
            Skill.level,
            Skill.can_teach,
            Skill.want_learn,
            func.count(skill_user_association.c.user_id).label("users_count"),
        )
        .outerjoin(skill_user_association, Skill.id == skill_user_association.c.skill_id)
        .group_by(Skill.id)
        .order_by(func.count(skill_user_association.c.user_id).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "rank": idx + 1,
            "skill_id": row.id,
            "title": row.title,
            "category": row.category,
            "level": row.level.value if hasattr(row.level, "value") else row.level,
            "can_teach": row.can_teach,
            "want_learn": row.want_learn,
            "users_count": row.users_count,
        }
        for idx, row in enumerate(rows)
    ]


async def get_active_users(db: AsyncSession, limit: int = 10) -> list[dict]:
    """Найактивніші користувачі за кількістю обмінів + відгуків."""
    exchanges_subq = (
        select(
            func.coalesce(Exchange.sender_id, Exchange.receiver_id).label("user_id"),
            func.count(Exchange.id).label("exchange_count"),
        )
        .where(
            (Exchange.sender_id != None) | (Exchange.receiver_id != None)
        )
        .group_by(Exchange.sender_id, Exchange.receiver_id)
    ).subquery()

    # Рахуємо кількість обмінів де юзер є sender або receiver
    sent_stmt = (
        select(
            Exchange.sender_id.label("user_id"),
            func.count(Exchange.id).label("cnt"),
        )
        .group_by(Exchange.sender_id)
    ).subquery()

    received_stmt = (
        select(
            Exchange.receiver_id.label("user_id"),
            func.count(Exchange.id).label("cnt"),
        )
        .group_by(Exchange.receiver_id)
    ).subquery()

    reviews_subq = (
        select(
            Review.reviewer_id.label("user_id"),
            func.count(Review.id).label("review_count"),
        )
        .group_by(Review.reviewer_id)
    ).subquery()

    skills_subq = (
        select(
            skill_user_association.c.user_id,
            func.count(skill_user_association.c.skill_id).label("skills_count"),
        )
        .group_by(skill_user_association.c.user_id)
    ).subquery()

    stmt = (
        select(
            User.id,
            User.username,
            User.full_name,
            func.coalesce(sent_stmt.c.cnt, 0).label("sent_exchanges"),
            func.coalesce(received_stmt.c.cnt, 0).label("received_exchanges"),
            func.coalesce(reviews_subq.c.review_count, 0).label("reviews_given"),
            func.coalesce(skills_subq.c.skills_count, 0).label("skills_count"),
            (
                func.coalesce(sent_stmt.c.cnt, 0)
                + func.coalesce(received_stmt.c.cnt, 0)
                + func.coalesce(reviews_subq.c.review_count, 0)
            ).label("activity_score"),
        )
        .outerjoin(sent_stmt, User.id == sent_stmt.c.user_id)
        .outerjoin(received_stmt, User.id == received_stmt.c.user_id)
        .outerjoin(reviews_subq, User.id == reviews_subq.c.user_id)
        .outerjoin(skills_subq, User.id == skills_subq.c.user_id)
        .order_by(
            (
                func.coalesce(sent_stmt.c.cnt, 0)
                + func.coalesce(received_stmt.c.cnt, 0)
                + func.coalesce(reviews_subq.c.review_count, 0)
            ).desc()
        )
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "rank": idx + 1,
            "user_id": row.id,
            "username": row.username,
            "full_name": row.full_name,
            "sent_exchanges": row.sent_exchanges,
            "received_exchanges": row.received_exchanges,
            "total_exchanges": row.sent_exchanges + row.received_exchanges,
            "reviews_given": row.reviews_given,
            "skills_count": row.skills_count,
            "activity_score": row.activity_score,
        }
        for idx, row in enumerate(rows)
    ]


async def get_exchange_success_rate(db: AsyncSession) -> dict:
    """Відсоток успішних обмінів та розбивка по статусах."""
    stmt = select(
        func.count(Exchange.id).label("total"),
        func.sum(
            case((Exchange.status == ExchangeStatus.completed.value, 1), else_=0)
        ).label("completed"),
        func.sum(
            case((Exchange.status == ExchangeStatus.pending.value, 1), else_=0)
        ).label("pending"),
        func.sum(
            case((Exchange.status == ExchangeStatus.accepted.value, 1), else_=0)
        ).label("accepted"),
        func.sum(
            case((Exchange.status == ExchangeStatus.rejected.value, 1), else_=0)
        ).label("rejected"),
        func.sum(
            case((Exchange.status == ExchangeStatus.cancelled.value, 1), else_=0)
        ).label("cancelled"),
    )

    result = await db.execute(stmt)
    row = result.first()

    total = row.total or 0
    completed = int(row.completed or 0)
    pending = int(row.pending or 0)
    accepted = int(row.accepted or 0)
    rejected = int(row.rejected or 0)
    cancelled = int(row.cancelled or 0)

    success_rate = round((completed / total * 100), 2) if total > 0 else 0.0
    failure_rate = round(((rejected + cancelled) / total * 100), 2) if total > 0 else 0.0

    return {
        "total_exchanges": total,
        "success_rate_percent": success_rate,
        "failure_rate_percent": failure_rate,
        "breakdown": {
            "completed": completed,
            "pending": pending,
            "accepted": accepted,
            "rejected": rejected,
            "cancelled": cancelled,
        },
    }