import subprocess
import os

# Define the root directory based on the location of the script
ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))

# Define paths for the agent, listener, and output directories
SERVER_DIR: str = os.path.join(ROOT_DIR, "bin-server")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

# List of platforms to compile for, specifying OS, architecture, and output file name
PLATFORMS = [
    ("windows", "386"),
    ("windows", "amd64"),
    ("linux", "386"),
    ("linux", "amd64"),
]


def run_command(command, env=None):
    """
    Executes a command in the shell and prints the output or error message.

    :param command: The shell command to execute.
    :param env: Optional environment variables to set for the command.
    """
    # Run the command and capture output and error
    result = subprocess.run(
        command, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Print an error message if the command failed, otherwise print the output
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr.decode()}")
    else:
        print(result.stdout.decode())


def compile_go_module(go_module_path, output_dir):
    """
    Compiles a Go module for multiple platforms and outputs the binaries to the specified directory.

    :param go_module_path: Path to the Go module to compile.
    :param output_dir: Directory to save the compiled binaries.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Change to the Go module directory
    os.chdir(go_module_path)

    # Get the module name from the directory name
    module_name = os.path.basename(go_module_path)

    # Build the Go module for each specified platform
    for goos, goarch in PLATFORMS:
        env = os.environ.copy()
        env["GOOS"] = goos
        env["GOARCH"] = goarch
        output_path = os.path.join(
            output_dir,
            f"{module_name}-{goos}-{goarch}"
            + (".exe" if goos == "windows" else ".bin"),
        )
        command = f'go build -ldflags="-s -w" -o {output_path}'
        print(f"Building for {goos}/{goarch}...")
        run_command(command, env)


if __name__ == "__main__":
    # Compile the agent and listener Go modules
    compile_go_module(SERVER_DIR, OUTPUT_DIR)
