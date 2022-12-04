import json
import flet as ft

class Task(ft.UserControl):
    def __init__(self, tsk: str, del_task, done = False) -> None:
        super().__init__()
        self.task = tsk
        self.del_task = del_task
        self.done = done

    def build(self) -> None:
        self.display_task = ft.Checkbox(
            value = self.done, label = self.task,
            check_color = 'green', on_change = self.mark_done
        )
        self.edit_task = ft.TextField(expand = True)
        
        self.display_view = ft.Row(
            alignment = 'spaceBetween',
            vertical_alignment = 'center',
            controls = [
                self.display_task,
                ft.Row(
                    spacing = 0,
                    controls = [
                        ft.IconButton(
                            icon = ft.icons.CREATE_OUTLINED,
                            tooltip = 'Edit task',
                            on_click = self.edit
                        ),
                        ft.IconButton(
                            icon = ft.icons.DELETE_OUTLINE,
                            tooltip = 'Remove task',
                            on_click = self.remove_task
                        )
                    ]
                )
            ]
        )

        self.edit_view = ft.Row(
            visible = False,
            alignment = 'spaceBetween',
            vertical_alignment = 'center',
            controls = [
                self.edit_task,
                ft.IconButton(
                    icon = ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color = ft.colors.GREEN,
                    tooltip = 'Edit task',
                    on_click = self.save
                )
            ]
        )

        return ft.Column(
            controls = [self.display_view, self.edit_view]
        )
    
    def edit(self, e) -> None:
        self.edit_task.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save(self, e) -> None:
        tasks = json.load(open('tasks.json'))['tasks']
        self.display_task.label = self.edit_task.value
        self.display_view.visible = True
        self.edit_view.visible = False
        ind = tasks.index(
            {
                'task': self.task,
                'done': self.done
            }
        )
        tasks[ind]['task'] = self.edit_task.value
        json.dump({'tasks': tasks}, open('tasks.json', 'w'))
        self.update()

    def remove_task(self, e): self.del_task(self)

    def mark_done(self, e) -> None:
        tasks = json.load(open('tasks.json'))['tasks']
        ind = tasks.index(
            {
                'task': self.task,
                'done': self.done
            }
        )
        self.done = not self.done
        tasks[ind]['done'] = self.done
        json.dump({'tasks': tasks}, open('tasks.json', 'w'))