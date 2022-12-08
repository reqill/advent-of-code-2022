import "./App.css";
import { input as inputTxt } from "./input";
import { input1 } from "./input1";

enum ItemType {
  DIRECTORY = "DIRECTORY",
  FILE = "FILE",
}

type FileType = {
  name: string;
  size: number;
  type: ItemType;
  path: string;
};
type DirectoryType = {
  files: (FileType | DirectoryType)[];
} & FileType;

const directories = /^dir\s.*$/gm;
const listFiles = /^\$ ls$/gm;
const moveUp = "$ cd ..";
const changeDirectory = /^\$ cd\s.*$/gm;

enum LineType {
  DIRECTORY = "DIRECTORY",
  FILE = "FILE",
  LIST_FILES = "LIST_FILES",
  MOVE_UP = "MOVE_UP",
  CHANGE_DIRECTORY = "CHANGE_DIRECTORY",
}

const getLineType = (line: string): LineType => {
  if (line.startsWith("dir ")) {
    return LineType.DIRECTORY;
  } else if (listFiles.test(line)) {
    return LineType.LIST_FILES;
  } else if (line === moveUp) {
    return LineType.MOVE_UP;
  } else if (line.startsWith("$ cd ") && !line.includes("..")) {
    return LineType.CHANGE_DIRECTORY;
  } else if (!line.startsWith("$")) {
    return LineType.FILE;
  }
  throw new Error("Unknown line type: " + line);
};

const mapObjectLocationToPath = (
  name: string,
  parent: DirectoryType
): string => {
  return `${parent.path}/${name}`;
};

const getDirectoryFromPath = (
  childPath: string,
  root: DirectoryType,
  getParent = false
): DirectoryType => {
  let pathParts = childPath.split("/");
  if (getParent) {
    pathParts = pathParts.slice(0, pathParts.length - 1);
  }

  let currentDirectory = root;

  for (const path of pathParts) {
    if (path === "root") continue;

    const currentDirectoryFile = currentDirectory.files.find(
      (file) => file.name === path && file.type === ItemType.DIRECTORY
    );

    if (currentDirectoryFile) {
      currentDirectory = currentDirectoryFile as DirectoryType;
    } else {
      console.error(root);
      throw new Error(
        `Path does not point to a directory ${path} || ${pathParts} \n${JSON.stringify(
          currentDirectory,
          null,
          " "
        )}\n${JSON.stringify(currentDirectoryFile, null, " ")}`
      );
    }
  }

  return currentDirectory;
};

const mapDirectoryStructure = (input: string, debug = false): DirectoryType => {
  const root: DirectoryType = {
    name: "root",
    size: 0,
    type: ItemType.DIRECTORY,
    path: "root",
    files: [],
  };
  let currentDirectory = root;
  const lines = input.split("\n");

  for (let i = 1; i < lines.length; i++) {
    const currentLine = lines[i];
    if (debug) {
      console.warn(
        "Line",
        i,
        "out of",
        lines.length,
        "\nCurrent commad/outupt:",
        currentLine
      );
    }

    switch (getLineType(currentLine)) {
      case LineType.DIRECTORY: {
        const directoryName = currentLine.split(" ")[1];
        const directory: DirectoryType = {
          name: directoryName,
          size: 0,
          type: ItemType.DIRECTORY,
          path: mapObjectLocationToPath(directoryName, currentDirectory),
          files: [],
        };

        currentDirectory.files.push(directory);
        break;
      }
      case LineType.FILE: {
        const [size, fileName] = currentLine.split(" ");
        const file: FileType = {
          name: fileName,
          size: parseInt(size) || 0,
          type: ItemType.FILE,
          path: mapObjectLocationToPath(fileName, currentDirectory),
        };

        currentDirectory.files.push(file);
        break;
      }
      case LineType.LIST_FILES: {
        break;
      }
      case LineType.MOVE_UP: {
        currentDirectory.size = currentDirectory.files.reduce(
          (acc, file) => acc + file.size,
          0
        );
        currentDirectory = getDirectoryFromPath(
          currentDirectory.path,
          root,
          true
        );
        break;
      }
      case LineType.CHANGE_DIRECTORY: {
        currentDirectory.size = currentDirectory.files.reduce(
          (acc, file) => acc + file.size,
          0
        );
        const directoryName = currentLine.split(" ")[2];
        currentDirectory = getDirectoryFromPath(
          mapObjectLocationToPath(directoryName, currentDirectory),
          root
        );
        break;
      }
    }
  }

  currentDirectory.size = currentDirectory.files.reduce(
    (acc, file) => acc + file.size,
    0
  );

  return root;
};

const findAllDirectoriesWhichSizeSatisfies = (
  root: DirectoryType,
  compare: (x: number) => boolean
): DirectoryType[] => {
  let matchingDirectories: DirectoryType[] = [];

  const findDirectories = (directory: DirectoryType) => {
    if (compare(directory.size)) {
      matchingDirectories.push(directory);
    }

    for (const file of directory.files) {
      if (file.type === ItemType.DIRECTORY) {
        findDirectories(file as DirectoryType);
      }
    }
  };

  findDirectories(root);

  return matchingDirectories;
};

function App() {
  const directoryStructure = mapDirectoryStructure(inputTxt);
  const dirSizeAtLMost100000 = findAllDirectoriesWhichSizeSatisfies(
    directoryStructure,
    (x) => x <= 100000
  );
  const smallDirsCombinedSize = dirSizeAtLMost100000.reduce(
    (acc, dir) => acc + dir.size,
    0
  );
  const wholeDirSize = directoryStructure.size;
  const updateSize = 30000000;
  const maxSize = 70000000;
  const spaceMoreNeeded = Math.abs(maxSize - (wholeDirSize + updateSize));
  const deleteFilesCandidates = findAllDirectoriesWhichSizeSatisfies(
    directoryStructure,
    (x) => x >= spaceMoreNeeded
  );

  deleteFilesCandidates.sort((a, b) => a.size - b.size);

  console.log("Root structure:", directoryStructure);
  console.log(
    "Sum of sizes of directories under 100000:",
    smallDirsCombinedSize
  );
  console.log("Root size:", wholeDirSize);
  console.log("Nedded update more size for update:", spaceMoreNeeded);
  console.log("You can delete files from:", deleteFilesCandidates);
  console.log(
    "Smallest directory to delete:",
    deleteFilesCandidates[0],
    "\nSize:",
    deleteFilesCandidates[0].size
  );

  return (
    <main className="App" style={{ whiteSpace: "pre", textAlign: "left" }}>
      <code>{JSON.stringify(directoryStructure, null, "  ")}</code>
    </main>
  );
}

export default App;
