import os

import tmt

class ReportDisplay(tmt.steps.report.ReportPlugin):
    """
    Show test results on the terminal

    Give a concise summary of test results directly on the terminal.
    List individual test results in verbose mode.
    """

    # Supported methods
    _methods = [tmt.steps.Method(name='display', doc=__doc__, order=50)]

    def details(self, result, verbosity):
        """ Print result details based on the verbose mode """
        # -v prints just result + name
        # -vv prints path to logs
        # -vvv prints also content of out.log
        self.verbose(result.show(), shift=1)
        if verbosity == 1:
            return
        # -vv and more follows
        for log_file in result.log:
            log_name = os.path.basename(log_file)
            full_path = os.path.join(self.step.plan.execute.workdir, log_file)
            # List path to logs (-vv and more)
            self.verbose(log_name, full_path, color='yellow', shift=2)
            # Show content of out.log (-vvv and more)
            if verbosity > 2 and log_name in ['out.log']:
                self.verbose(
                    'content', self.read(full_path), color='yellow', shift=2)

    def go(self):
        """ Discover available tests """
        super().go()
        # Show individual test results only in verbose mode
        if not self.opt('verbose'):
            return
        for result in self.step.plan.execute.results():
            self.details(result, self.opt('verbose'))
