"""
Learning Service
Generates structured learning paths for various subjects
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from ..models.database import (
    LearningPath, LearningTopic, Example, Exercise, MiniProject, ReviewQuestion
)


class LearningService:
    """Service for generating and managing learning paths."""

    def __init__(self):
        # Predefined learning paths
        self.subject_templates = {
            "linear_algebra": self._linear_algebra_template,
            "neural_networks": self._neural_networks_template,
            "operating_systems": self._operating_systems_template,
            "c_programming": self._c_programming_template,
            "physics": self._physics_template,
            "calculus": self._calculus_template,
            "algorithms": self._algorithms_template,
            "data_structures": self._data_structures_template,
        }

    def generate_path(
        self, subject: str, difficulty: str = "beginner"
    ) -> Optional[LearningPath]:
        """Generate a learning path for the given subject."""
        subject_key = subject.lower().replace(" ", "_")

        if subject_key not in self.subject_templates:
            return None

        template_func = self.subject_templates[subject_key]
        path = template_func(difficulty)

        return path

    def _linear_algebra_template(self, difficulty: str) -> LearningPath:
        """Linear algebra learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="linear_algebra",
            title="Linear Algebra",
            description="Master vectors, matrices, and linear transformations",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Vectors and Vector Spaces",
                    explanation="A vector is an ordered list of numbers representing a point or direction in space. A vector space is a collection of vectors that can be added and scaled.",
                    prerequisites=[],
                    examples=[
                        Example(
                            title="Vector Addition",
                            description="Adding two vectors component-wise",
                            code="v1 = [1, 2, 3]\nv2 = [4, 5, 6]\nresult = [a + b for a, b in zip(v1, v2)]",
                            output="[5, 7, 9]",
                            explanation="Component-wise addition of vectors"
                        ),
                    ],
                    exercises=[
                        Exercise(
                            title="Compute Vector Magnitude",
                            description="Write code to compute the magnitude of a vector.",
                            hints=["Use the formula |v| = sqrt(x^2 + y^2 + ...)"],
                            difficulty="easy"
                        ),
                    ],
                    mini_projects=[
                        MiniProject(
                            title="2D Vector Visualizer",
                            description="Create a simple program that visualizes 2D vectors and their operations",
                            requirements=["Plot vectors as arrows", "Show vector addition", "Show vector scaling"],
                            difficulty="beginner"
                        ),
                    ],
                    review_questions=[
                        ReviewQuestion(
                            question="What is a vector?",
                            answer="An ordered collection of numbers representing a point or direction in space."
                        ),
                    ],
                    order=1,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Matrices and Matrix Operations",
                    explanation="A matrix is a rectangular array of numbers arranged in rows and columns. Matrix operations include addition, multiplication, and transposition.",
                    prerequisites=["Vectors and Vector Spaces"],
                    examples=[
                        Example(
                            title="Matrix Multiplication",
                            description="Multiplying two matrices A and B",
                            code="A = [[1, 2], [3, 4]]\nB = [[5, 6], [7, 8]]\n# Result[i][j] = sum(A[i][k] * B[k][j])",
                            output="[[19, 22], [43, 50]]",
                            explanation="Each element of the result is the dot product of a row from A and a column from B"
                        ),
                    ],
                    exercises=[
                        Exercise(
                            title="Matrix Multiplication",
                            description="Implement matrix multiplication without using NumPy.",
                            difficulty="medium"
                        ),
                    ],
                    review_questions=[
                        ReviewQuestion(
                            question="What are the conditions for matrix multiplication?",
                            answer="The number of columns in the first matrix must equal the number of rows in the second matrix."
                        ),
                    ],
                    order=2,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Eigenvalues and Eigenvectors",
                    explanation="Eigenvectors are non-zero vectors that don't change direction when a linear transformation is applied. Eigenvalues are the scalar factors by which the eigenvectors are scaled.",
                    prerequisites=["Matrices and Matrix Operations", "Vectors and Vector Spaces"],
                    examples=[
                        Example(
                            title="Finding Eigenvalues",
                            description="Solve for eigenvalues of a 2x2 matrix",
                            code="import numpy as np\nA = np.array([[4, -2], [1, 1]])\neigenvalues, eigenvectors = np.linalg.eig(A)",
                            output="Eigenvalues: [3, 2]",
                            explanation="Use np.linalg.eig to find eigenvalues and eigenvectors"
                        ),
                    ],
                    review_questions=[
                        ReviewQuestion(
                            question="What does it mean for a vector to be an eigenvector?",
                            answer="An eigenvector remains on its own line after a linear transformation, only being scaled by the eigenvalue."
                        ),
                    ],
                    order=3,
                ),
            ],
        )
        return path

    def _neural_networks_template(self, difficulty: str) -> LearningPath:
        """Neural networks learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="neural_networks",
            title="Neural Networks",
            description="Understand the foundations of deep learning",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Perceptrons and Neurons",
                    explanation="A perceptron is the simplest type of artificial neuron, computing a weighted sum of inputs and applying a step function.",
                    prerequisites=["Linear Algebra"],
                    examples=[
                        Example(
                            title="Simple Perceptron",
                            description="A perceptron that learns the AND function",
                            code="import numpy as np\nclass Perceptron:\n    def __init__(self, n_inputs):\n        self.weights = np.zeros(n_inputs)\n        self.bias = 0\n    def predict(self, inputs):\n        activation = np.dot(self.weights, inputs) + self.bias\n        return 1 if activation > 0 else 0",
                            explanation="A basic perceptron implementation"
                        ),
                    ],
                    exercises=[
                        Exercise(
                            title="Implement AND Gate",
                            description="Train a perceptron to learn the AND logic gate.",
                            difficulty="easy"
                        ),
                    ],
                    review_questions=[
                        ReviewQuestion(
                            question="What is the role of activation functions?",
                            answer="Activation functions introduce non-linearity into the network, allowing it to learn complex patterns."
                        ),
                    ],
                    order=1,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Backpropagation",
                    explanation="Backpropagation is the algorithm used to train neural networks by computing gradients of the loss function with respect to weights.",
                    prerequisites=["Perceptrons and Neurons", "Calculus"],
                    examples=[
                        Example(
                            title="Chain Rule Application",
                            description="Computing gradients through multiple layers",
                            explanation="Gradients flow backwards through the network using the chain rule of calculus"
                        ),
                    ],
                    review_questions=[
                        ReviewQuestion(
                            question="What is the chain rule and how is it used in backpropagation?",
                            answer="The chain rule states that the derivative of a composite function is the product of derivatives. In backpropagation, it's used to compute gradients at each layer."
                        ),
                    ],
                    order=2,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Convolutional Neural Networks",
                    explanation="CNNs are specialized for processing grid-like data such as images, using convolutional layers to detect spatial patterns.",
                    prerequisites=["Backpropagation", "Linear Algebra"],
                    examples=[
                        Example(
                            title="Convolution Operation",
                            description="Applying a filter to detect edges in an image",
                            explanation="Convolutions slide a small filter over the input image to detect features"
                        ),
                    ],
                    review_questions=[
                        ReviewQuestion(
                            question="What advantages do CNNs have over fully connected networks for images?",
                            answer="CNNs use parameter sharing and local connectivity, dramatically reducing the number of parameters while preserving spatial relationships."
                        ),
                    ],
                    order=3,
                ),
            ],
        )
        return path

    def _operating_systems_template(self, difficulty: str) -> LearningPath:
        """Operating systems learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="operating_systems",
            title="Operating Systems",
            description="Process management, memory, file systems, and concurrency",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Processes and Threads",
                    explanation="A process is an instance of a running program. Threads are lightweight units of execution within a process.",
                    prerequisites=[],
                    review_questions=[
                        ReviewQuestion(
                            question="What is the difference between a process and a thread?",
                            answer="Processes have separate memory spaces; threads share memory within a process."
                        ),
                    ],
                    order=1,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Memory Management",
                    explanation="Memory management handles allocation and deallocation of memory to processes, including virtual memory and paging.",
                    prerequisites=["Processes and Threads"],
                    review_questions=[
                        ReviewQuestion(
                            question="What is virtual memory?",
                            answer="Virtual memory is a memory management technique that uses both hardware and software to allow a computer to compensate for physical memory shortages by temporarily transferring pages of data to disk storage."
                        ),
                    ],
                    order=2,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="File Systems",
                    explanation="File systems organize data on storage devices, managing files, directories, and metadata.",
                    prerequisites=["Memory Management"],
                    review_questions=[
                        ReviewQuestion(
                            question="What are the main components of a file system?",
                            answer="File systems include a data structure for files, metadata management, directory organization, and access control."
                        ),
                    ],
                    order=3,
                ),
            ],
        )
        return path

    def _c_programming_template(self, difficulty: str) -> LearningPath:
        """C programming learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="c_programming",
            title="C Programming",
            description="Master the C language for systems programming",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Variables and Data Types",
                    explanation="C provides basic data types like int, float, char, and double for storing different kinds of values.",
                    prerequisites=[],
                    examples=[
                        Example(
                            title="Variable Declaration",
                            description="Declaring and initializing variables in C",
                            code="int age = 25;\nfloat price = 19.99;\nchar initial = 'A';",
                            explanation="Variables must be declared with a type before use"
                        ),
                    ],
                    order=1,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Pointers and Memory",
                    explanation="Pointers are variables that store memory addresses. They are powerful but require careful management.",
                    prerequisites=["Variables and Data Types"],
                    examples=[
                        Example(
                            title="Pointer Basics",
                            description="Using pointers to access memory addresses",
                            code="int x = 10;\nint *ptr = &x;\nprintf(\"%d\", *ptr);  // Prints 10",
                            explanation="& takes the address, * dereferences the pointer"
                        ),
                    ],
                    order=2,
                ),
            ],
        )
        return path

    def _physics_template(self, difficulty: str) -> LearningPath:
        """Physics learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="physics",
            title="Physics",
            description="Mechanics, electromagnetism, and modern physics",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Classical Mechanics",
                    explanation="Classical mechanics describes the motion of macroscopic objects using Newton's laws.",
                    prerequisites=["Calculus"],
                    review_questions=[
                        ReviewQuestion(
                            question="What are Newton's three laws?",
                            answer="1) An object in motion stays in motion unless acted on. 2) F=ma. 3) For every action, an equal and opposite reaction."
                        ),
                    ],
                    order=1,
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Electromagnetism",
                    explanation="Electromagnetism describes the interaction of electric and magnetic fields.",
                    prerequisites=["Classical Mechanics", "Calculus"],
                    review_questions=[
                        ReviewQuestion(
                            question="What is Maxwell's equation?",
                            answer="Maxwell's equations are four equations that describe how electric and magnetic fields are generated and altered by each other and by charges and currents."
                        ),
                    ],
                    order=2,
                ),
            ],
        )
        return path

    def _calculus_template(self, difficulty: str) -> LearningPath:
        """Calculus learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="calculus",
            title="Calculus",
            description="Differential and integral calculus",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Limits and Continuity",
                    explanation="A limit describes the value a function approaches as input approaches some value.",
                    order=1,
                    review_questions=[
                        ReviewQuestion(
                            question="What is a limit?",
                            answer="A limit is the value that a function approaches as the input approaches some value."
                        ),
                    ],
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Derivatives",
                    explanation="The derivative measures the rate of change of a function.",
                    prerequisites=["Limits and Continuity"],
                    order=2,
                    review_questions=[
                        ReviewQuestion(
                            question="What does a derivative represent geometrically?",
                            answer="The slope of the tangent line at a point on the function's curve."
                        ),
                    ],
                ),
            ],
        )
        return path

    def _algorithms_template(self, difficulty: str) -> LearningPath:
        """Algorithms learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="algorithms",
            title="Algorithms",
            description="Classic algorithms and analysis",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Sorting Algorithms",
                    explanation="Sorting algorithms arrange elements in a specific order.",
                    order=1,
                    review_questions=[
                        ReviewQuestion(
                            question="What is the time complexity of merge sort?",
                            answer="O(n log n) in all cases."
                        ),
                    ],
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Graph Algorithms",
                    explanation="Graph algorithms solve problems on graph structures like BFS, DFS, and shortest path.",
                    prerequisites=["Sorting Algorithms", "Data Structures"],
                    order=2,
                    review_questions=[
                        ReviewQuestion(
                            question="What is BFS?",
                            answer="Breadth-first search explores all nodes at the present depth before moving to nodes at the next depth level."
                        ),
                    ],
                ),
            ],
        )
        return path

    def _data_structures_template(self, difficulty: str) -> LearningPath:
        """Data structures learning path."""
        path = LearningPath(
            id=str(uuid.uuid4()),
            subject="data_structures",
            title="Data Structures",
            description="Arrays, lists, trees, and graphs",
            difficulty=difficulty,
            topics=[
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Arrays and Lists",
                    explanation="Arrays store elements in contiguous memory. Linked lists use pointers to connect nodes.",
                    order=1,
                    review_questions=[
                        ReviewQuestion(
                            question="What's the difference between arrays and linked lists?",
                            answer="Arrays have O(1) random access but O(n) insertion. Linked lists have O(n) access but O(1) insertion at known positions."
                        ),
                    ],
                ),
                LearningTopic(
                    id=str(uuid.uuid4()),
                    title="Trees and Graphs",
                    explanation="Trees are hierarchical structures. Graphs represent networks of connected nodes.",
                    prerequisites=["Arrays and Lists"],
                    order=2,
                    review_questions=[
                        ReviewQuestion(
                            question="What is a binary search tree?",
                            answer="A binary search tree is a binary tree where for each node, all values in the left subtree are less and all values in the right subtree are greater."
                        ),
                    ],
                ),
            ],
        )
        return path

    def list_subjects(self) -> List[Dict[str, str]]:
        """List all available subjects."""
        return [
            {"id": key, "name": value.__name__.replace("_template", "").replace("_", " ").title()}
            for key, value in self.subject_templates.items()
        ]