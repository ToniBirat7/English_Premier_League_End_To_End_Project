import docker
from docker.errors import NotFound

def start_container(container_name):
    client = docker.from_env()

    # List all containers (debug)
    containers = client.containers.list(all=True)
    print("All containers:")
    for c in containers:
        print(f" - {c.name} ({c.status})")

    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            container.start()
            print(f"✅ Container '{container_name}' started.")
        else:
            print(f"ℹ️ Container '{container_name}' is already running.")
    except NotFound:
        print(f"❌ Container '{container_name}' not found.")
    except Exception as e:
        print(f"❌ Error starting container: {e}")

if __name__ == "__main__":
    start_container("main-mariadb")
