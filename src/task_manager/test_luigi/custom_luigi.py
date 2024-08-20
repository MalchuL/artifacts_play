import luigi

INT_VALUE = 0


class TaskA(luigi.Task):
    param = luigi.IntParameter()

    def run(self):
        print("A", INT_VALUE)
        with self.output().open("w") as f:
            f.write(str(INT_VALUE))

    def output(self):
        return luigi.LocalTarget(f"output_test/taskA{self.param}.txt")


class TaskC(luigi.Task):
    param = luigi.IntParameter()

    def run(self):
        with self.output().open("w") as f:
            f.write("ABOBA")

    def output(self):
        return luigi.LocalTarget("output_test/taskC.txt")


class TaskB(luigi.Task):
    param = luigi.IntParameter()

    def requires(self):
        return TaskA(param=self.param)

    def run(self):
        global INT_VALUE
        print("B", INT_VALUE)

        if INT_VALUE > 0:
            # with self.output().open("r") as f:
            #     lines = f.readlines
            with self.output().open("w") as f:
                f.write(str(INT_VALUE))
        else:
            INT_VALUE += 1
            print(INT_VALUE)
            # with self.output().open("w") as f:
            #     f.write(str(INT_VALUE))
            task = self.requires()
            task.output().remove()
            yield task
            print("Don't do anything")

    def output(self):
        return luigi.LocalTarget("output_test/taskB.txt")


if __name__ == "__main__":
    luigi.build([TaskB(param=8)], detailed_summary=True, log_level="DEBUG", local_scheduler=True)
