from typing import Union

from app.models import CharityProject
from app.models.donation import Donation


def investment(
    instance: Union[CharityProject, Donation],
    non_invested_list: list[Union[CharityProject, Donation]],
):
    if non_invested_list:
        for item in non_invested_list:
            instance_available_sum = instance.full_amount - instance.invested_amount
            item_available_sum = item.full_amount - item.invested_amount
            if instance_available_sum > item_available_sum:
                item.invested()
                non_invested_list.append(item)
                instance.invested_amount += item_available_sum
            elif instance_available_sum < item_available_sum:
                item.invested_amount += instance_available_sum
                instance.invested()
                non_invested_list.append(instance)
                return non_invested_list
            elif instance_available_sum == item_available_sum:
                item.invested()
                instance.invested()
                non_invested_list.append(instance)
                return non_invested_list
    non_invested_list.append(instance)
    return non_invested_list
