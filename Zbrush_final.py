import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from pathlib import Path

# to add : create new dir for projects that don't already exist



desktop_path = Path("/Users/bimbo/Desktop")
project_dir_path = Path("/Users/bimbo/Documents/Zbrush/Projects")

class Watcher:

    def __init__(self, directory=desktop_path, handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandlers(FileSystemEventHandler):



    def on_created(self, event):  # ".ZPR" Handler

        if event.src_path[-4:]==".zpr" or event.src_path[-4] == ".ZPR":
            new_zfile_name = event.src_path.split("/")
            new_zfile_name = new_zfile_name[-1]
            new_zfile_name_name, new_zfile_name_ext = os.path.splitext(new_zfile_name)
            # print(new_zfile_name_name)
            os.chdir("/Users/bimbo/Documents/Zbrush/Projects")
            for directory in os.listdir(os.getcwd()):
                # print(directory)
                if directory == new_zfile_name_name:

                    os.chdir(f"/Users/bimbo/Documents/Zbrush/Projects/{directory}")
                    # print(os.getcwd())
                    for existing_zfile in os.listdir(os.getcwd()):  # looping over files in existing project's dir
                        if existing_zfile == new_zfile_name:
                            os.remove(existing_zfile)
                            os.rename(f"/Users/bimbo/Desktop/{new_zfile_name}", f"/Users/bimbo/Documents/Zbrush/Projects/"
                                                                               f"{directory}/{new_zfile_name}")
                            print(f"The file {new_zfile_name} has been moved to the new location {project_dir_path/directory}")

                elif not os.path.isfile(project_dir_path/new_zfile_name_name):
                    os.chdir(project_dir_path)
                    os.mkdir(new_zfile_name_name)
                    os.rename(f"/Users/bimbo/Desktop/{new_zfile_name}", f"/Users/bimbo/Documents/Zbrush/Projects/{new_zfile_name_name}/{new_zfile_name}")

                    # Works but yields "FileExistsError: [Errno 17] File exists:" and doesn't let previous block to execute

                else:
                    os.rename(f"/Users/bimbo/Desktop/{new_zfile_name}", f"/Users/bimbo/Documents/Zbrush/Projects/To_organise/{new_zfile_name}")





if __name__ == "__main__":
    w = Watcher(desktop_path, MyHandlers())
    w.run()

