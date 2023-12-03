from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.crud.charity_project import charity_project_crud


async def donation_investment_calculation(
    donate: Donation, session: AsyncSession
):
    donate_sum = donate.full_amount
    while donate_sum != 0:
        project = await charity_project_crud.get_first_unfilled(session)
        if project:
            project, donate = await donation_distribution(
                project=project,
                donate=donate,
                donate_sum=donate_sum,
                session=session,
            )
            donate_sum -= donate.invested_amount
        else:
            break


async def project_investment_calculation(
    project: CharityProject, session: AsyncSession
):
    donations = await donation_crud.get_multi_unused_donations(session)
    loop_indicator = 0
    while not project.fully_invested and len(donations) >= loop_indicator + 1:
        donate = donations[loop_indicator]
        donate_sum = donate.full_amount - donate.invested_amount
        project, donate = await donation_distribution(
            project=project,
            donate=donate,
            donate_sum=donate_sum,
            session=session,
        )
        loop_indicator += 1
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def donation_distribution(
    project: CharityProject,
    donate: Donation,
    donate_sum: Donation,
    session: AsyncSession,
):
    invest_sum = project.full_amount - project.invested_amount
    if invest_sum < donate_sum:
        donate_sum -= invest_sum
    else:
        donate.fully_invested = True
    donate.invested_amount += donate_sum
    project.invested_amount += donate_sum
    if project.full_amount == project.invested_amount:
        project.close_date = datetime.now()
        project.fully_invested = True
    session.add(donate)
    await session.commit()
    await session.refresh(donate)
    return project, donate
