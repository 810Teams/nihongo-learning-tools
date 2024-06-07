"""
    `src/service/operation_service.py`
"""

from custom.append import custom_append_head
from src.core.app_data import OperationList
from src.service.backup_service import BackupService
from src.model.operation import Operation
from src.core.app_data import OPERATION_LIST
from src.model.command import Command
from src.model.parameter import Parameter
from src.model.storage import Storage
from src.service.render_service import RenderService
from src.util.logging import error, notice
from src.util.reader import convert_csv_to_list
from settings import DEFAULT_AVERAGE_RANGE, DEFAULT_DAYS, DEFAULT_DOTS_COUNT, DEFAULT_MAX_Y_LABELS, DEFAULT_STYLE, DEFAULT_X_LABEL


class OperationService:
    def __init__(self, storage: Storage) -> None:
        self.storage: Storage = storage
        self.render_service: RenderService = RenderService(storage)
        self.backup_service: BackupService = BackupService(storage)

    def execute(self, command: Command) -> None:
        """ Method: Validate and execute command """
        print()
        if self._find_operation(command) is None:
            error('Command \'{}\' error.'.format(command.name))
            error('Please check if the command exists.')
        elif not self._validate_command(command):
            error('Command \'{}\' error.'.format(command.name))
            error('Please check value types of the command as well as its arguments.')
        else:
            exec('self._operate_{}(command)'.format(command.name))
            self.backup_service.backup()

    def _operate_append(self, command: Command) -> None:
        """ Method: Operation Code 'A' (Add Data) """
        value = command.value

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
        """ Method: Operation Code 'C' (Create Charts) """
        parameter_list = OperationList.Chart.ParameterList

        self.render_service.render_all(
            allow_float=command.contains_argument(parameter_list.allow_float.name),
            average_range=self._get_argument_variable(command, parameter_list.average_range, DEFAULT_AVERAGE_RANGE),
            days=self._get_argument_variable(command, parameter_list.days, DEFAULT_DAYS),
            is_dynamic=command.contains_argument(parameter_list.dynamic.name),
            is_today=command.contains_argument(parameter_list.today.name),
            dots_count=self._get_argument_variable(command, parameter_list.dots_count, DEFAULT_DOTS_COUNT),
            max_y_labels=self._get_argument_variable(command, parameter_list.max_y, DEFAULT_MAX_Y_LABELS),
            style=self._get_argument_variable(command, parameter_list.style, DEFAULT_STYLE),
            x_label=self._get_argument_variable(command, parameter_list.x_label, DEFAULT_X_LABEL)
        )

    def _operate_reload(self, command: Command) -> None:
        """ Method: Operation Code 'R' (Reload Storage) """
        self.storage.reload()
        notice('Storage \'{}\' is reloaded from disk.'.format(self.storage.name))

    def _operate_save(self, command: Command) -> None:
        """ Method: Operation Code 'S' (Save Storage) """
        self.storage.save()
        notice('Storage \'{}\' is saved to disk.'.format(self.storage.name))

    def _operate_sync(self, command: Command) -> None:
        """ Method: Operation Code 'S' (Sync) """
        self.backup_service.load_backup()

    def _operate_view(self, command: Command) -> None:
        """ Method: Operation Code 'V' (View Storage) """
        print()
        print(self.storage.data)

    def _operate_exit(self, command: Command) -> None:
        """ Method: Operation Code 'X' (Exit) """
        notice('Exitting application.')
        exit()

    def _validate_command(self, command: Command) -> bool:
        """ Method: Validate command """
        operation: Operation = self._find_operation(command)

        if operation is None:
            return False

        return operation.validate_command(command)

    def _find_operation(self, command: Command) -> Operation:
        """ Method: Find operation """
        operation: Operation
        for operation in OPERATION_LIST:
            if command.name == operation.name:
                return operation
        return None

    def _get_argument_variable(self, command: Command, parameter: Parameter, default_value: any) -> any:
        """ Method: Decide argument value based on argument in command and default value """
        if command.contains_argument(parameter.name):
            return parameter.value_type(command.get_argument(parameter.name).value)
        return default_value
