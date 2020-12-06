from luigi import LocalTarget


class Requirement:
    def __init__(self, task_class, **params):
        self.task = task_class
        self.params = params

    def __get__(self, task, cls):
        if task is None:
            return self
        return task.clone(self.task, **self.params)


class Requires:
    """Composition to replace :meth:`luigi.task.Task.requires`
    Example::
        class MyTask(Task):
            # Replace task.requires()
            requires = Requires()
            other = Requirement(OtherTask)
            def run(self):
                # Convenient access here...
                with self.other.output().open('r') as f:
                    ...
        MyTask().requires()
        {'other': OtherTask()}
    """

    def __get__(self, task, cls):
        if task is None:
            return self

        # Bind self/task in a closure
        return lambda: self(task)

    def __call__(self, task):
        """Returns the requirements of a task
        Assumes the task class has :class:`.Requirement` descriptors, which
        can clone the appropriate dependences from the task instance.
        :returns: requirements compatible with `task.requires()`
        :rtype: dict
        """

        return {
            k: getattr(task, k)
            for k, v in task.__class__.__dict__.items()
            if isinstance(v, Requirement)
        }
