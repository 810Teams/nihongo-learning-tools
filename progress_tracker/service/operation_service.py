"""
    `progress_tracker/service/operation_service.py`
"""

from typing import Any

from core.base.operation_service_base import OperationServiceBase
from core.model.command import Command
from core.util.format import path
from core.util.logging import error, notice
from progress_tracker.constant.app_data import OPERATION_LIST, CHART_BASE_PATH, OperationList
from progress_tracker.custom.append import custom_append_head
from progress_tracker.model.storage import Storage
from progress_tracker.service.backup_service import BackupService
from progress_tracker.service.render_service import RenderService
from progress_tracker.settings import *
from progress_tracker.util.reader import convert_csv_to_list


class OperationService(OperationServiceBase):
    def __init__(self, storage: Storage) -> None:
        super().__init__(OPERATION_LIST)
        self.storage: Storage = storage
        self.render_service: RenderService = RenderService(storage)
        self.backup_service: BackupService = BackupService(storage)

    def _operate_append(self, command: Command) -> None:
        """ Method: Add Data """
        value: Any = command.value

        if command.contains_argument(OperationList.Append.ParameterList.add.name):
            try:
                value = convert_csv_to_list(value, value_type=int, replace_null=0)
                initial = self.storage.to_list()[-1][1:]
                new_row = [int(initial[i]) + value[i] for i in range(len(initial))]
                self.storage.append(new_row)
                notice('Data {} is added to the storage.'.format(new_row))
            except ValueError:
                error('Invalid value format. Please try again.')

        elif command.contains_argument(OperationList.Append.ParameterList.custom.name):
            try:
                custom_id = int(command.get_argument(OperationList.Append.ParameterList.custom.name).value)
                if custom_id not in (1, 2, 3, 4, 5):
                    error('Custom ID must be an integer from 1 to 5.')
                    return
            except (IndexError, ValueError):
                error('Custom ID must be an integer.')
                return

            try:
                new_row = custom_append_head(value, custom_id)
                self.storage.append(new_row)
                notice('Data {} is added to the storage.'.format(new_row))
            except IndexError:
                error('Invalid value format. Please try again.')
                error('Function \'custom_append_{}\' might not have been implemented.'.format(custom_id))

        else:
            try:
                new_row = convert_csv_to_list(value, value_type=int, replace_null=0)
                self.storage.append(new_row)
                notice('Data {} is added to the storage.'.format(new_row))
            except ValueError:
                error('Invalid value format. Please try again.')

    def _operate_chart(self, command: Command) -> None:
        """ Method: Create Charts """
        parameter_list = OperationList.Chart.ParameterList

        if command.contains_argument(parameter_list.open_only.name):
            notice('Opening chart files.')
            super()._open_file(path(CHART_BASE_PATH, '*'))
            return

        self.render_service.render_all(
            allow_float=command.contains_argument(parameter_list.allow_float.name),
            average_range=super()._get_argument_value(command, parameter_list.average_range),
            days=super()._get_argument_value(command, parameter_list.days),
            is_dynamic=command.contains_argument(parameter_list.dynamic.name),
            is_today=command.contains_argument(parameter_list.today.name),
            dots_count=super()._get_argument_value(command, parameter_list.dots_count),
            max_y_labels=super()._get_argument_value(command, parameter_list.max_y),
            style=super()._get_argument_value(command, parameter_list.style),
            x_label=super()._get_argument_value(command, parameter_list.x_label)
        )

        if command.contains_argument(parameter_list.open.name):
            notice('Opening chart files.')
            self._open_file(path(CHART_BASE_PATH, '*'))

    def _operate_open(self, command: Command) -> None:
        """ Method: Open storage file """
        notice('Opening storage file.')
        super()._open_file(self.storage.get_path())

    def _operate_reload(self, command: Command) -> None:
        """ Method: Reload Storage """
        self.storage.reload()
        notice('Storage \'{}\' is reloaded from disk.'.format(self.storage.name))

    def _operate_save(self, command: Command) -> None:
        """ Method: Save Storage """
        self.storage.save()
        notice('Storage \'{}\' is saved to disk.'.format(self.storage.name))
        self.backup_service.backup()
        notice('Storage \'{}\' is automatically backed up to the designated path.'.format(self.storage.name))

    def _operate_sync(self, command: Command) -> None:
        """ Method: Load Backup Storage File """
        self.backup_service.load_backup()

    def _operate_view(self, command: Command) -> None:
        """ Method: View Storage """
        print(self.storage.data)
