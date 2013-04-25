from kaylee.project import Project, AUTO_PROJECT_MODE
from kaylee.errors import InvalidResultError

class Pi_Calc(Project):
    mode = AUTO_PROJECT_MODE

    def __init__(self, *args, **kwargs):
        super(Pi_Calc, self).__init__(*args, **kwargs)

        self.client_config.update({

        })

    def next_task(self):
        pass

    def __getitem__(self, task_id):
        return {
            'id' : 'obligatory_task_id_here'
        }

    def normalize_result(self, task_id, result):
        raise InvalidResultError(result, 'The result is invalid.')

    def result_stored(self, task_id, result, storage):
        pass
