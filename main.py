from afs import AFS

import typer
import os

app = typer.Typer()


@app.command("extract")
def extract(filepath: str):
    try:
        os.mkdir("extracted")
    except:
        pass

    with open(filepath, "rb") as f:
        afs = AFS(f)

        for file in afs.files:
            afs.move_to_position(file["offset"])

            with open("extracted/" + file["filename"], "wb") as ff:
                ff.write(afs.read_bytes(file["length"]))
            
            print("Extracted", file["filename"])


if __name__ == "__main__":
    app()
