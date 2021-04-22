import sys
import os
import pathlib
import glob

INSERTION_TAG = "% {insert_listing}"

# Supported languages and their corresponding extensions (cf. Pygment)
SUPPORTED_LANGUAGES = ["python", "cpp", "html"] 
SUPPORTED_EXTENSIONS = [".py", ".cpp", ".txt"]
HIERARCHY_COMPONENTS = ["section", "subsection", "subsubsection"]

# Set to true if you want to display the hierarchy in LaTeX
ADD_HIERARCHY = True


class Node:
	name = ""
	fpath = ""
	cleaned_fpath = ""
	isLeaf = False
	parent = None
	children = []
	depth = -1
	language = ""
	ext = ""

	def __init__(self, name, parent, depth):
		self.name = name
		self.parent = parent
		self.isLeaf = False
		self.children = []
		self.depth = depth
		self.language = ""
		self.ext = ""


# Explore the hierarchy tree and display the listings
def exploreNode(node: Node):
	if node.isLeaf:
		caption = node.cleaned_fpath.replace('\\', '\\textbackslash ') \
								.replace('_', '\\_')
		cleaned_fpath = node.cleaned_fpath.replace("\\", "_")\
									.replace("/", "_") \
									.replace(".", "_") 
		label=f"code:{cleaned_fpath}"

		header = ("\\begin{code}\n"
		f"\\captionof{{listing}}{{{caption}}}\n"
		f"\\label{{{label}}}\n"
		f"\\begin{{minted}}{{{node.language}}}\n")

		dest_file.write(header)
		f = open(node.fpath, 'r')
		dest_file.write(f.read())
		f.close()

		footer = "\n\\end{minted}\n\\end{code}\n\n"
		dest_file.write(footer)
	else:
		for child in node.children:
			if not child.isLeaf and ADD_HIERARCHY:
				cleaned_name = child.name.replace("_", "\\textunderscore ")
				hierarchy_depth = min(child.depth, len(HIERARCHY_COMPONENTS)-1)
				dest_file.write(f"\\{HIERARCHY_COMPONENTS[hierarchy_depth]}{{" + cleaned_name + "}\n")
			exploreNode(child)

# Sort nodes according to their depth
def sortNodes (node: Node):
	if not node.isLeaf:
		node.children.sort(key=(lambda x: (not x.isLeaf, x.name)))
		for child in node.children:
			sortNodes(child)


if __name__ == "__main__":
	if len(sys.argv) != 4:
		raise Exception("Wrong number of arguments. Usage: RELATIVE_PATH DEST_PATH TEMPLATE_PATH")
	path = sys.argv[1]
	dest_path = sys.argv[2]
	template_path = sys.argv[3]

	dest_file = open(dest_path, 'w')
	template_file = open(template_path, 'r')

	template = template_file.read()
	insertion_pos = template.find(INSERTION_TAG)
	if insertion_pos == -1:
		raise Exception(f"Cannot find the insertion tag in the template. In your template, please add: {INSERTION_TAG}")

	dest_file.write(template[:insertion_pos])

	root = Node("", None, -1)

	for (i_ext, ext) in enumerate(SUPPORTED_EXTENSIONS):
		filepaths = glob.glob(path+'/**/*'+ext, recursive=True)
		for fpath in filepaths:
			cleaned_fpath = fpath[len(path) + 1:]

			# TODO: add option depending on OS
			hierarchy = cleaned_fpath.split("\\")
			parent = root
			for (i_h, a) in enumerate(hierarchy):
				a_exists = False
				for child in parent.children:
					if a == child.name:
						parent = child
						a_exists = True
						break
				if not a_exists:
					node = Node(a, parent, parent.depth + 1)
					parent.children.append(node)
					parent = node
					if i_h == len(hierarchy) - 1:
						node.isLeaf = True
						node.fpath = fpath
						node.cleaned_fpath = cleaned_fpath
						node.ext = ext
						node.language = SUPPORTED_LANGUAGES[i_ext]

	sortNodes(root)
	exploreNode(root)

	dest_file.write(template[insertion_pos+len(INSERTION_TAG):])

	dest_file.close()