import subprocess
import sys

def func(submission, examples):
    code = submission.answer

    for example in examples:
        cin = example.input + "\n" if example.input else ""
        cout = example.output or ""

        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                input=cin,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                print("STDERR:", result.stderr)
                return 'ERROR'

            if result.stdout.strip() != cout.strip():
                return 'not all'

        except Exception as error:
            print("EXCEPTION:", error)
            return 'ERROR'

    return 'complete'
