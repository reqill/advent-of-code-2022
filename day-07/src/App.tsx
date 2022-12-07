import "./App.css";
import { input as inputTxt } from "./input";

enum Type {
  Directory = "directory",
  File = "file",
}

type FileType = { name: string; size: number; type: Type };
type DirectoryType = {
  files?: (FileType | DirectoryType)[];
  parent?: DirectoryType;
} & FileType;

const commands = /\$.*$/gm;
const output = /^(?!$).*(?<!$).*$/gm;
const directories = /^dir\s.*$/gm;
const files = /^\d+\s.*\..*$/gm;
const listFiles = /^\$ ls$/gm;
const moveUp = /^\$ cd \.\.$/gm;
const changeDirectory = /^\$ cd\s.*$/gm;

const mapDirectoryStructure = (lines: string[]): DirectoryType => {
  console.log("Statred mapping...");
  const root: DirectoryType = {
    type: Type.Directory,
    name: "root",
    size: 0,
    files: [],
  };
  let currentDirectory = root;
  let currentLine = 1;

  while (currentLine < lines.length) {
    const line = lines[currentLine];
    const isCommand = line.match(commands);
    const isOutput = line.match(output);

    console.warn(`Line ${currentLine} out of ${lines.length}`);
    console.log(line);

    if (isCommand) {
      const isListFiles = line.match(listFiles);
      const isMoveUp = line.match(moveUp);
      const isChangeDirectory = line.match(changeDirectory);

      if (isListFiles) {
        console.log("Listing files in directory", currentDirectory);
        currentLine++;
        continue;
      } else if (isMoveUp) {
        currentDirectory = currentDirectory.parent!;
        console.log("Moving up to directory", currentDirectory);

        currentLine++;
        continue;
      } else if (isChangeDirectory) {
        const where = line.split(" ")[2]!;
        if (currentDirectory.files) {
          currentDirectory = currentDirectory.files.find(
            (dir: any) => dir.name === where
          )!;
        }
        console.log("Changing directory to", currentDirectory, where);
        currentLine++;
        continue;
      }

      currentLine++;
      continue;
    } else if (isOutput) {
      const isDirectory = line.match(directories);
      const isFile = line.match(files);

      if (isDirectory) {
        const name = line.split(" ")[1]!;
        const directory: DirectoryType = {
          type: Type.Directory,
          name,
          size: 0,
          files: [],
          parent: currentDirectory,
        };
        // push new directory if it doesn't exist
        if (
          !currentDirectory.files?.some((file) => file.name === directory.name)
        ) {
          currentDirectory.files?.push(directory);
        }

        currentLine++;
        continue;
      } else if (isFile) {
        const size = Number(line.split(" ")[0])!;
        const name = line.split(" ")[1]!;
        const file: FileType = { type: Type.File, name, size };

        if (currentDirectory.files) {
          currentDirectory.files!.push(file);
        }
        currentDirectory.size += size;

        currentLine++;
        continue;
      }

      currentLine++;
      continue;
    }

    currentLine++;
  }
  return root;
};

const parseInput = (input: string): string[] => {
  const lines = input.split("\n");
  return lines;
};

const remapWholeNestedObjectWithoutProperty = (
  obj: DirectoryType,
  property: keyof DirectoryType
): DirectoryType => {
  const newObj = { ...obj };
  delete newObj[property];
  if (newObj?.files) {
    newObj.files = newObj?.files.map((file) => {
      //@ts-ignore
      if (file?.files) {
        return remapWholeNestedObjectWithoutProperty(file, property);
      }
      return file;
    });
  }
  return newObj;
};

function App() {
  const lines = remapWholeNestedObjectWithoutProperty(
    mapDirectoryStructure(parseInput(inputTxt)),
    "parent"
  );
  console.log(lines);
  return (
    <main className="App" style={{ whiteSpace: "pre", textAlign: "left" }}>
      <code>{JSON.stringify(lines.files, null, "  ")}</code>
    </main>
  );
}

export default App;
