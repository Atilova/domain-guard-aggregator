from infrastructure.db.models.securitytrails import SecurityTrailsAccountModel

from sqlalchemy import select, func


total_available_request_query = (
    select(
        SecurityTrailsAccountModel,        
        func.sum(SecurityTrailsAccountModel.available_requests).over(
            order_by=SecurityTrailsAccountModel.sign_up_date
        ).label('total_available_requests')
    )
    .where(SecurityTrailsAccountModel.is_active == True)
    .select_from(SecurityTrailsAccountModel)
    .alias('total_available_request_query')
)

def select_at_least_n_available_requests(at_least: int):
    """select_at_least_n_available_requests"""

    return (
        select(
            total_available_request_query.c,
            total_available_request_query.c.total_available_requests
        )
        .where(
            (total_available_request_query.c.total_available_requests <= at_least) |
            total_available_request_query.c.id.in_(
                select(total_available_request_query.c.id)
                .where(total_available_request_query.c.total_available_requests >= at_least)
                .limit(1)
            )
        )
    )