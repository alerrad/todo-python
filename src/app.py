import flet as ft, json
from taskModel import Task

tasks = json.load(open('tasks.json'))['tasks']

def main(page: ft.Page):
    page.title = 'To-do app'
    page.horizontal_alignment = 'center'
    page.window_center()
    
    def remove_task(task: Task) -> None:
        tasks_container.controls.remove(task)
        tasks.remove(
            {
                'task': task.task,
                'done': task.done
            }
        )
        json.dump({'tasks': tasks}, open('tasks.json', 'w'))
        page.update()

    def add_task(e) -> None:
        tasks_container.controls.append(Task(
            tsk = new_task.value,
            del_task = remove_task
        ))
        tasks.append(
            {
                'task': new_task.value,
                'done': False
            }
        )
        json.dump({'tasks': tasks}, open('tasks.json', 'w'))
        new_task.value = ''
        page.update()

    new_task = ft.TextField(hint_text = 'Enter task',
    expand = True, height = 45, content_padding = 10)
    tasks_container = ft.Column(expand = True) # insert tasks here
    
    # Parse json
    for task in tasks:
        tasks_container.controls.append(Task(
            tsk = task['task'],
            del_task = remove_task,
            done = task['done']
        ))

    page.add(
        ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        new_task,
                        ft.FloatingActionButton(
                            icon = ft.icons.ADD,
                            on_click = add_task,
                            height = 45,
                            width = 45
                        )
                    ]
                ),
                tasks_container
            ],
            width = 600
        )
    )

if __name__ == '__main__':
    print('App started!')
    ft.app(target = main)