"""
    `src/service/operation_service.py`
"""

from custom.append import custom_append_head
from src.core.app_data import OperationList
from src.service.backup_service import BackupService
from src.model.operation import Operation
from src.core.app_data import OPERATION_LIST
from src.model.command import Command
from src.model.storage import Storage
from src.service.render_service import RenderService
from src.util.logging import error, notice
from src.util.reader import convert_csv_to_list
from settings import DEFAULT_AVERAGE_RANGE, DEFAULT_DAYS, DEFAULT_DOTS_COUNT, DEFAULT_MAX_Y_LABELS, DEFAULT_STYLE, DEFAULT_X_LABEL


class OperationService:
    def __init__(self, storage: Storage) -> None:
        self.storage: Storage = storage
        self.render_service: RenderService = RenderService(storage)
        self.backup_service: BackupService = BackupService(storage.name)

    def execute(self, command: Command) -> None:
        """ Method: Validate and execute command """
        print()
        if self.find_operation(command) is None:
            error('Command \'{}\' error.'.format(command.name))
            error('Please check if the command exists.')
        elif not self.validate_command(command):
            error('Command \'{}\' error.'.format(command.name))
            error('Please check value types of the command as well as its arguments.')
        else:
            exec('self.operate_{}(command)'.format(command.name))
            self.backup_service.trigger_backup()

    def operate_append(self, command: Command) -> None:
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

    def operate_chart(self, command: Command) -> None:
        """ Method: Operation Code 'C' (Create Charts) """
        # Step 1: -average argument
        average_range = DEFAULT_AVERAGE_RANGE
        if command.contains_argument(OperationList.Chart.ParameterList.average_range.name):
            try:
                average_range = int(command.get_argument(OperationList.Chart.ParameterList.average_range.name).value)
            except ValueError:
                error('Average range must be an integer.')
                error('Aborting chart creation process.')
                return

        # Step 2: -days argument
        days = DEFAULT_DAYS
        if command.contains_argument(OperationList.Chart.ParameterList.days.name):
            try:
                days = OperationList.Chart.ParameterList.days.value_type(command.get_argument(OperationList.Chart.ParameterList.days.name).value)
            except ValueError:
                error('Duration must be an {}.'.format(OperationList.Chart.ParameterList.days.value_type))
                error('Aborting chart creation process.')
                return

        # Step 3: -dots-count argument
        dots_count = DEFAULT_DOTS_COUNT
        if command.contains_argument(OperationList.Chart.ParameterList.dots_count.name):
            try:
                dots_count = int(command.get_argument(OperationList.Chart.ParameterList.dots_count.name).value)
            except ValueError:
                error('Maximum dots must be an integer.')
                error('Aborting chart creation process.')
                return

        # Step 4: -max-y argument
        max_y_labels = DEFAULT_MAX_Y_LABELS
        if command.contains_argument(OperationList.Chart.ParameterList.max_y.name):
            try:
                max_y_labels = int(command.get_argument(OperationList.Chart.ParameterList.max_y.name).value)
            except ValueError:
                error('Maximum y labels must be an integer.')
                error('Aborting chart creation process.')
                return

        # Step 5: -style argument
        style = DEFAULT_STYLE
        if command.contains_argument(OperationList.Chart.ParameterList.style.name):
            style = command.get_argument(OperationList.Chart.ParameterList.style.name).value

        # Step 6: -x-label argument
        x_label = DEFAULT_X_LABEL
        if command.contains_argument(OperationList.Chart.ParameterList.x_label.name):
            x_label = command.get_argument(OperationList.Chart.ParameterList.x_label.name).value

        # Step 7: Render charts
        self.render_service.render_all(
            allow_float=command.contains_argument(OperationList.Chart.ParameterList.allow_float.name),
            average_range=average_range,
            days=days,
            is_dynamic=command.contains_argument(OperationList.Chart.ParameterList.dynamic.name),
            is_today=command.contains_argument(OperationList.Chart.ParameterList.today.name),
            dots_count=dots_count,
            max_y_labels=max_y_labels,
            style=style,
            x_label=x_label
        )

    def operate_reload(self, command: Command) -> None:
        """ Method: Operation Code 'R' (Reload Storage) """
        self.storage.reload()
        notice('Storage \'{}\' is reloaded from disk.'.format(self.storage.name))

    def operate_save(self, command: Command) -> None:
        """ Method: Operation Code 'S' (Save Storage) """
        self.storage.save()
        notice('Storage \'{}\' is saved to disk.'.format(self.storage.name))

    def operate_view(self, command: Command) -> None:
        """ Method: Operation Code 'V' (View Storage) """
        print()
        print(self.storage.data)

    def operate_exit(self, command: Command) -> None:
        """ Method: Operation Code 'X' (Exit) """
        notice('Exitting application.')
        exit()

    def validate_command(self, command: Command) -> bool:
        """ Method: Validate command """
        operation: Operation = self.find_operation(command)

        if operation is None:
            return False

        return operation.validate_command(command)

    def find_operation(self, command: Command) -> Operation:
        """ Method: Find operation """
        operation: Operation
        for operation in OPERATION_LIST:
            if command.name == operation.name:
                return operation
        return None
