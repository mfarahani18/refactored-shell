import subprocess


class JobManager:
    def __init__(self):
        self.jobs_data = {}

    def run_background(
        self, command, args, original_command
    ):
        process = subprocess.Popen(
            [command, *args[:-1]]
        )

        if not self.jobs_data:
            job_number = 1
        else:
            job_number = max(self.jobs_data.keys()) + 1

        self.jobs_data[job_number] = {
            "process": process,
            "pid": process.pid,
            "command": original_command,
            "status": "running",
        }

        return f"[{job_number}] {process.pid}"

    def reap_jobs(self):
        job_numbers = list(self.jobs_data.keys())
        finished_jobs = []

        for job_number, data in self.jobs_data.items():
            if data["process"].poll() is not None:
                self.print_done_job(
                    job_number, data, job_numbers
                )
                finished_jobs.append(job_number)

        for job_number in finished_jobs:
            del self.jobs_data[job_number]

    def jobs(self):
        job_numbers = list(self.jobs_data.keys())
        finished_jobs = []

        for job_number, data in self.jobs_data.items():
            if data["process"].poll() is None:
                self.print_running_job(
                    job_number, data, job_numbers
                )
            else:
                self.print_done_job(
                    job_number, data, job_numbers
                )
                finished_jobs.append(job_number)

        for job_number in finished_jobs:
            del self.jobs_data[job_number]

    def job_marker(self, job_number, job_numbers):
        if job_number == job_numbers[-1]:
            return "+"

        if (
            len(job_numbers) > 1
            and job_number == job_numbers[-2]
        ):
            return "-"

        return " "

    def print_running_job(
        self, job_number, data, job_numbers
    ):
        status = f"{data['status']:<24}"
        marker = self.job_marker(
            job_number, job_numbers
        )

        print(
            f"[{job_number}]{marker}  "
            f"{status}{data['command']}"
        )

    def print_done_job(
        self, job_number, data, job_numbers
    ):
        status = f"{'Done':<24}"
        done_command = data["command"].rstrip(" &")
        marker = self.job_marker(
            job_number, job_numbers
        )

        print(
            f"[{job_number}]{marker}  "
            f"{status}{done_command}"
        )
