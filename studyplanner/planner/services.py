import logging
from datetime import date, timedelta, datetime, time
from .models import StudySession

logger = logging.getLogger(__name__)

DIFFICULTY_MULTIPLIERS = {1: 1.0, 2: 2.0, 3: 3.5}
CONCENTRATION_FACTORS  = [(3, 1.5), (7, 1.2)]

STUDY_SLOTS = [
    (time(6, 0),  time(8, 0)),
    (time(9, 0),  time(11, 0)),
    (time(12, 0), time(14, 0)),
    (time(15, 0), time(17, 0)),
    (time(18, 0), time(20, 0)),
    (time(20, 0), time(22, 0)),
]

# ── TOPIC-SPECIFIC STEPS ─────────────────────────────
TOPIC_STEPS = {
    "python": {
        "Syntax & Basics":     ["Install Python and setup VS Code", "Variables and data types — int, float, str, bool", "Type conversion and input() function", "Comments and indentation rules"],
        "Strings":             ["String creation and indexing", "String slicing and negative indexing", "String methods — upper, lower, strip, split", "f-strings and format() method"],
        "Lists & Tuples":      ["Create and access lists", "List methods — append, insert, remove, pop", "List slicing and copying", "Tuples — immutability and use cases"],
        "Dictionaries":        ["Create dictionaries and access values", "Dictionary methods — keys, values, items", "Add, update and delete entries", "Iterate through dictionaries with loops"],
        "Loops":               ["for loop with range()", "for loop over lists and strings", "while loop and conditions", "break, continue and pass statements", "Nested loops and pattern printing"],
        "Functions":           ["Define functions with def keyword", "Parameters and return values", "Default and keyword arguments", "*args and **kwargs usage", "Lambda functions and map/filter"],
        "OOP":                 ["Classes and objects — basics", "Constructor __init__ and self keyword", "Instance vs class variables", "Inheritance and super()", "Polymorphism and method overriding", "Encapsulation and dunder methods"],
        "File Handling":       ["Open and read files with open()", "Write and append to files", "Working with CSV files", "Using with statement — context manager", "os module for file operations"],
        "Exception Handling":  ["try/except basics", "Multiple except blocks", "finally and else blocks", "raise custom exceptions", "Create your own Exception class"],
        "Modules":             ["import and from import syntax", "Built-in modules — os, sys, math, random", "Installing packages with pip", "Creating your own module", "Virtual environments setup"],
        "List Comprehensions": ["Basic list comprehension syntax", "Conditional list comprehensions", "Nested list comprehensions", "Dictionary and set comprehensions", "Generator expressions"],
        "Recursion":           ["Base case and recursive case", "Factorial using recursion", "Fibonacci sequence recursively", "Binary search recursively", "When recursion vs loops"],
        "Projects":            ["Build a calculator app", "Build a to-do list CLI", "Number guessing game", "File-based student records", "Simple contact book"],
    },
    "java": {
        "Basics":             ["JDK setup and Hello World", "Variables, data types and type casting", "Operators — arithmetic, relational, logical", "Control flow — if/else and switch", "Loops — for, while, do-while"],
        "OOP":                ["Classes and objects basics", "Constructors and this keyword", "Inheritance and super keyword", "Method overloading and overriding", "Abstract classes and interfaces", "Polymorphism and encapsulation"],
        "Arrays & Strings":   ["1D array declaration and iteration", "2D arrays and matrix operations", "String class and common methods", "StringBuilder for mutable strings", "String comparison and manipulation"],
        "Collections":        ["ArrayList — add, remove, iterate", "LinkedList operations", "HashMap — key-value pairs", "HashSet for unique elements", "Collections utility methods — sort, reverse"],
        "Exception Handling": ["try/catch/finally basics", "Checked vs unchecked exceptions", "throw and throws keywords", "Custom exception classes", "Multi-catch blocks"],
        "File I/O":           ["FileReader and FileWriter basics", "BufferedReader for efficient reading", "BufferedWriter for writing", "File class — create, delete, exists", "Serialization and deserialization"],
        "Multithreading":     ["Thread class and Runnable interface", "Creating and starting threads", "Thread lifecycle — states", "synchronized keyword", "wait, notify and notifyAll"],
        "Java 8 Features":    ["Lambda expressions syntax", "Functional interfaces", "Stream API — filter, map, collect", "Optional class usage", "Method references"],
        "Projects":           ["Bank account system", "Student management with ArrayList", "Calculator with OOP", "File-based inventory system", "Multi-threaded task runner"],
    },
    "javascript": {
        "Basics":           ["Variables — var, let, const differences", "Data types and typeof operator", "Operators and expressions", "Conditionals — if/else, ternary", "Loops — for, while, for...of, for...in"],
        "DOM":              ["Select elements — getElementById, querySelector", "Modify text — textContent, innerHTML", "Change CSS styles with JS", "Add/remove CSS classes — classList", "Create and append new elements", "Remove elements — remove()"],
        "Functions":        ["Function declarations vs expressions", "Arrow functions syntax", "Default parameters", "Closures and lexical scope", "Higher order functions — map, filter, reduce"],
        "Arrays & Objects": ["Array methods — push, pop, shift, unshift", "Array methods — map, filter, reduce", "find, some, every, includes", "Object creation and dot/bracket access", "Destructuring arrays and objects", "Spread and rest operators"],
        "Async JS":         ["setTimeout and setInterval", "Promises — then, catch, finally", "async/await syntax", "Fetch API for HTTP GET request", "POST request with fetch and JSON", "Error handling in async code"],
        "ES6+":             ["Template literals", "Modules — import and export", "Classes and OOP in JS", "Map and Set data structures", "Optional chaining ?. and nullish coalescing ??"],
        "Projects":         ["Todo app with local storage", "Quiz app with scoring", "Weather app using fetch API", "Calculator with DOM", "Expense tracker app"],
    },
    "c programming": {
        "Basics":           ["GCC setup and Hello World", "Variables, data types and format specifiers", "Arithmetic and relational operators", "Input with scanf, output with printf", "Type conversion — implicit and explicit"],
        "Control Flow":     ["if/else and nested conditions", "switch/case statements", "for loop with examples", "while and do-while loops", "break and continue statements"],
        "Functions":        ["Function declaration and definition", "Pass by value parameters", "Return types and void functions", "Recursive functions — factorial, fibonacci", "Scope — local vs global variables"],
        "Arrays & Strings": ["1D array declaration and access", "Array iteration and searching", "2D arrays and matrix operations", "Strings as char arrays", "String functions — strlen, strcpy, strcat, strcmp"],
        "Pointers":         ["Pointer declaration and dereferencing", "Pointer arithmetic", "Pointers and arrays relationship", "Pointers as function parameters", "Pointer to pointer — double pointer"],
        "Structures":       ["struct declaration and member access", "Array of structures", "Nested structures", "Structures with functions", "typedef for cleaner code"],
        "File Handling":    ["fopen and fclose", "Reading with fscanf and fgets", "Writing with fprintf and fputs", "Binary file read and write", "File error handling with errno"],
        "Data Structures":  ["Linked list — node creation and insertion", "Singly linked list — delete and traverse", "Stack using arrays — push and pop", "Queue using arrays — enqueue and dequeue", "Bubble sort and selection sort"],
    },
    "c++": {
        "Basics":          ["Hello World, namespaces, cin/cout", "Variables, data types, references", "Operators and type conversions", "Control flow — if/else, switch, loops", "Functions — overloading, default args"],
        "OOP":             ["Classes and objects", "Constructors and destructors", "Encapsulation — access modifiers", "Inheritance — single and multiple", "Polymorphism — virtual functions", "Abstract classes and pure virtual"],
        "STL":             ["vector — push_back, pop_back, iterate", "list and deque", "map and unordered_map", "set and unordered_set", "STL algorithms — sort, find, count"],
        "Templates":       ["Function templates", "Class templates", "Template specialization", "Variadic templates basics", "SFINAE concept basics"],
        "Memory":          ["Dynamic memory — new and delete", "Smart pointers — unique_ptr", "shared_ptr and weak_ptr", "RAII principle", "Memory leaks and valgrind"],
        "Modern C++":      ["Lambda expressions", "Move semantics and rvalue references", "auto and decltype", "Range-based for loop", "Structured bindings"],
        "File I/O":        ["ifstream and ofstream", "Reading line by line", "Writing formatted output", "Binary file operations", "File error handling"],
        "Projects":        ["Matrix calculator", "Student management with STL", "Bank system using OOP", "Simple compiler/interpreter", "Template-based data structure library"],
    },
    "data structures": {
        "Arrays":          ["Array basics and memory layout", "Insertion and deletion in arrays", "Linear and binary search", "Sorting — bubble and selection", "2D arrays and matrix problems"],
        "Linked Lists":    ["Singly linked list — node structure", "Insert at beginning, end, middle", "Delete by value and position", "Reverse a linked list", "Doubly and circular linked list"],
        "Stacks & Queues": ["Stack using arrays — push and pop", "Stack using linked list", "Balanced parentheses problem", "Queue — enqueue and dequeue", "Circular queue and deque"],
        "Trees":           ["Binary tree — node structure", "Inorder, preorder, postorder traversal", "Binary search tree — insert, search", "BST deletion", "Height and level order traversal"],
        "Graphs":          ["Adjacency matrix representation", "Adjacency list representation", "BFS traversal with queue", "DFS traversal with stack/recursion", "Cycle detection"],
        "Hashing":         ["Hash function basics", "Collision handling — chaining", "Open addressing — linear probing", "Load factor and rehashing", "HashMap implementation from scratch"],
        "Sorting":         ["Bubble, selection, insertion sort", "Merge sort — divide and conquer", "Quick sort — pivot and partition", "Heap sort", "Time complexity comparison of all sorts"],
        "Searching":       ["Linear search", "Binary search — iterative", "Binary search — recursive", "Search in rotated sorted array", "Two pointer and sliding window"],
    },
    "algorithms": {
        "Complexity":          ["Big O notation — O(1), O(n), O(log n)", "Time vs space complexity", "Best, average, worst case analysis", "Amortized analysis", "Recurrence relations — Master theorem"],
        "Divide & Conquer":    ["Merge sort implementation", "Quick sort with different pivots", "Binary search variations", "Closest pair of points", "Karatsuba multiplication"],
        "Greedy":              ["Activity selection problem", "Fractional knapsack", "Huffman coding", "Dijkstra's shortest path", "Prim's MST"],
        "Dynamic Programming": ["Memoization vs tabulation", "0/1 Knapsack problem", "Longest common subsequence", "Longest increasing subsequence", "Matrix chain multiplication", "Coin change problem"],
        "Graph Algorithms":    ["BFS and DFS implementation", "Dijkstra's shortest path", "Bellman-Ford algorithm", "Floyd-Warshall all pairs", "Kruskal's MST with union-find"],
        "Backtracking":        ["N-Queens problem", "Sudoku solver", "Rat in a maze", "Subset sum problem", "Permutations and combinations"],
        "String Algorithms":   ["KMP pattern matching", "Rabin-Karp rolling hash", "Z-algorithm", "Longest palindromic substring", "Edit distance"],
        "Bit Manipulation":    ["AND, OR, XOR operations", "Left and right shift", "Check and set bits", "Count set bits — Brian Kernighan", "Power of 2 and other tricks"],
    },
    "machine learning": {
        "Python for ML":      ["NumPy — arrays, reshape, operations", "Pandas — DataFrame, read_csv, groupby", "Matplotlib — line, bar, scatter plots", "Seaborn — heatmap, pairplot", "Scikit-learn pipeline overview"],
        "Data Preprocessing": ["Handle missing values — fillna, dropna", "Encode categorical — LabelEncoder, OneHot", "Feature scaling — MinMaxScaler, StandardScaler", "Train/test split — test_size, stratify", "Feature selection — SelectKBest"],
        "Regression":         ["Linear regression theory — cost function", "Implement with sklearn LinearRegression", "Multiple linear regression", "Polynomial regression", "Evaluate — MSE, RMSE, R² score"],
        "Classification":     ["Logistic regression — sigmoid function", "Decision tree — Gini and entropy", "Random forest — n_estimators, max_depth", "SVM — kernel trick", "KNN — choosing K value"],
        "Clustering":         ["K-means — centroid initialization", "Elbow method for optimal K", "Hierarchical — dendrogram", "DBSCAN — eps and min_samples", "Silhouette score evaluation"],
        "Neural Networks":    ["Perceptron — weights and bias", "Activation functions — ReLU, sigmoid, softmax", "Feedforward network with Keras", "Compile — optimizer, loss, metrics", "Train with fit() and evaluate"],
        "Model Evaluation":   ["Confusion matrix — TP, TN, FP, FN", "Precision, recall, F1-score", "ROC curve and AUC score", "K-fold cross validation", "GridSearchCV hyperparameter tuning"],
        "Projects":           ["House price prediction — regression", "Spam classifier — NLP + logistic", "Iris classification — decision tree", "Customer segmentation — K-means", "Digit recognition — neural network"],
    },
    "web development": {
        "HTML":       ["Document structure — DOCTYPE, html, head, body", "Text tags — h1-h6, p, span, strong", "Links, images and media", "Lists — ol, ul, dl", "Tables and semantic HTML5 elements", "Forms — input types and attributes"],
        "CSS":        ["Selectors — class, id, attribute, pseudo", "Box model — margin, padding, border", "Flexbox — justify-content, align-items", "CSS Grid — grid-template-columns, rows", "Responsive — media queries and breakpoints", "Animations — keyframes and transitions"],
        "JavaScript": ["DOM selection and manipulation", "Event listeners — click, input, submit", "Fetch API for REST calls", "Form validation with JS", "ES6 features in practice"],
        "React":      ["Create React App and file structure", "Components, JSX and props", "useState and useEffect hooks", "Fetch data and render list", "React Router for navigation"],
        "Node.js":    ["Node setup — require, module.exports", "npm — install, package.json scripts", "Express — app.get, app.post", "Middleware — cors, body-parser", "Connect to MongoDB with Mongoose"],
        "Databases":  ["SQL — SELECT, JOIN, aggregate", "MongoDB — insertOne, find, updateOne", "Mongoose schema and model", "CRUD operations end-to-end", "Indexing for performance"],
        "Git":        ["git init, add, commit, status", "Branching — branch, checkout, merge", "Remote — push, pull, clone", "Pull requests and code review", "Resolving merge conflicts"],
        "Deployment": ["Vercel for frontend deployment", "Render for backend deployment", "Environment variables — .env", "CORS setup for cross-origin", "Domain and HTTPS basics"],
    },
    "react": {
        "JSX & Components":  ["JSX syntax and expressions", "Functional components", "Fragment and conditional rendering", "Component composition", "Passing children prop"],
        "Props & State":     ["Passing and destructuring props", "PropTypes for type checking", "useState — initial state and updater", "State with objects and arrays", "Lifting state up to parent"],
        "Hooks":             ["useEffect — fetch on mount", "useEffect cleanup function", "useContext — createContext and Provider", "useReducer for complex state", "Custom hooks — extract logic"],
        "Routing":           ["BrowserRouter and Routes setup", "Route, Link and NavLink", "useParams — dynamic routes", "useNavigate — programmatic navigation", "Protected route pattern"],
        "State Management":  ["Context API — Provider and Consumer", "Redux store and actions", "Redux Toolkit — createSlice", "useSelector and useDispatch", "Redux Thunk for async"],
        "API Calls":         ["useEffect with fetch GET request", "Axios — axios.get and axios.post", "Loading and error state pattern", "Abort controller for cleanup", "Custom useFetch hook"],
        "Performance":       ["React.memo — prevent re-renders", "useMemo — memoize calculations", "useCallback — stable function refs", "Lazy loading with React.lazy", "Code splitting with Suspense"],
        "Projects":          ["Todo app — full CRUD", "Weather dashboard with search", "Authentication flow — login/logout", "E-commerce product listing", "Full stack with Django REST"],
    },
    "sql": {
        "Basics":              ["CREATE TABLE — data types and NOT NULL", "INSERT INTO — single and multiple rows", "SELECT — all columns and specific", "UPDATE — SET with WHERE condition", "DELETE — with and without WHERE"],
        "Filtering & Sorting": ["WHERE — comparison operators", "AND, OR, NOT logic", "LIKE — % and _ wildcards", "IN, BETWEEN, IS NULL", "ORDER BY ASC/DESC and LIMIT"],
        "Joins":               ["INNER JOIN — matching rows only", "LEFT JOIN — all left + matched right", "RIGHT JOIN — all right + matched left", "FULL OUTER JOIN", "Self join for hierarchical data"],
        "Aggregation":         ["COUNT(*) and COUNT(column)", "SUM, AVG, MAX, MIN", "GROUP BY with aggregate", "HAVING to filter grouped results", "DISTINCT to remove duplicates"],
        "Subqueries":          ["Subquery in WHERE clause", "Subquery in FROM — derived table", "Correlated subquery", "EXISTS and NOT EXISTS", "Subquery vs JOIN performance"],
        "Advanced SQL":        ["Views — CREATE VIEW and usage", "Indexes — CREATE INDEX, EXPLAIN", "Stored procedures — IN/OUT params", "Triggers — BEFORE/AFTER INSERT", "Window functions — ROW_NUMBER, RANK, LAG"],
        "Database Design":     ["ER diagram — entities and relationships", "Primary key and foreign key", "One-to-many with foreign key", "Many-to-many with junction table", "Normalization — 1NF, 2NF, 3NF"],
        "Projects":            ["Library management system", "E-commerce schema and queries", "Student result management", "Hospital appointment system", "Inventory tracking system"],
    },
    "physics": {
        "Mechanics":           ["Units, dimensions and significant figures", "Kinematics — equations of motion", "Newton's laws — inertia, F=ma, reaction", "Work, energy and power", "Conservation of momentum and collisions"],
        "Thermodynamics":      ["Heat transfer — conduction, convection, radiation", "Specific heat and calorimetry", "First law — ΔU = Q - W", "Second law and entropy", "Carnot engine efficiency"],
        "Waves & Sound":       ["Wave properties — amplitude, frequency, wavelength", "Speed of sound in different media", "Doppler effect — moving source/observer", "Resonance and standing waves", "Beats and superposition"],
        "Electrostatics":      ["Coulomb's law and electric force", "Electric field lines and intensity", "Electric potential and potential energy", "Capacitors in series and parallel", "Energy stored in capacitor"],
        "Current Electricity": ["Ohm's law V=IR", "Resistors in series and parallel", "Kirchhoff's current law — KCL", "Kirchhoff's voltage law — KVL", "Wheatstone bridge"],
        "Magnetism":           ["Magnetic field — sources and field lines", "Force on moving charge — F=qvB", "Force on current-carrying conductor", "Biot-Savart law", "Faraday's law of induction"],
        "Optics":              ["Reflection — laws and mirror formula", "Refraction — Snell's law", "Total internal reflection", "Lens formula and power", "Ray diagrams for lenses and mirrors"],
        "Modern Physics":      ["Photoelectric effect — Einstein's equation", "de Broglie wavelength", "Bohr model of hydrogen atom", "Radioactivity — alpha, beta, gamma decay", "Nuclear fission and fusion energy"],
    },
    "chemistry": {
        "Atomic Structure":     ["Subatomic particles and atomic number", "Bohr model and energy levels", "Quantum numbers — n, l, m, s", "Aufbau principle and electronic configuration", "Periodic trends — atomic radius, IE, EN"],
        "Chemical Bonding":     ["Ionic bonding — lattice energy", "Covalent bonding — Lewis structures", "VSEPR theory — molecular geometry", "Hybridization — sp, sp2, sp3", "Intermolecular forces — H-bond, van der Waals"],
        "States of Matter":     ["Kinetic molecular theory", "Gas laws — Boyle, Charles, Gay-Lussac", "Ideal gas equation PV=nRT", "Real gases — van der Waals equation", "Liquids and solids — properties"],
        "Thermochemistry":      ["Enthalpy — exothermic and endothermic", "Hess's law and Born-Haber cycle", "Standard enthalpy of formation", "Bond energies and lattice energy", "Gibbs free energy ΔG = ΔH - TΔS"],
        "Equilibrium":          ["Dynamic equilibrium concept", "Kc and Kp expressions", "Le Chatelier's principle", "Acid-base equilibrium — Ka, Kb, Kw", "Buffer solutions and Henderson equation"],
        "Electrochemistry":     ["Oxidation states and redox reactions", "Balancing redox — half-reaction method", "Galvanic cell — anode, cathode, EMF", "Nernst equation", "Electrolysis — Faraday's laws"],
        "Organic Chemistry":    ["IUPAC nomenclature — alkanes, alkenes, alkynes", "Functional groups — alcohol, aldehyde, ketone", "Carboxylic acids and derivatives", "Aromatic compounds — benzene and reactions", "Polymers — addition and condensation"],
        "Reaction Mechanisms":  ["SN1 and SN2 nucleophilic substitution", "Electrophilic addition to alkenes", "Elimination reactions E1 and E2", "Free radical halogenation", "Electrophilic aromatic substitution"],
    },
    "mathematics": {
        "Algebra":             ["Polynomials — operations and factor theorem", "Quadratic equations — discriminant and roots", "Sequences — AP: nth term and sum", "GP — nth term, sum, infinite GP", "Logarithms — properties and equations"],
        "Trigonometry":        ["Trigonometric ratios — sin, cos, tan", "Pythagorean and reciprocal identities", "Compound and double angle formulas", "Inverse trig functions — domain and range", "Solving trig equations"],
        "Coordinate Geometry": ["Distance, midpoint and section formula", "Straight lines — slope and different forms", "Angle between lines and perpendicular distance", "Circles — standard and general form", "Parabola, ellipse and hyperbola"],
        "Calculus":            ["Limits — definition and standard limits", "Continuity and differentiability", "Differentiation rules — chain, product, quotient", "Applications — maxima, minima, rate of change", "Integration — substitution and by parts", "Definite integrals and area under curve"],
        "Vectors":             ["Vector addition and subtraction", "Scalar multiplication and unit vectors", "Dot product and angle between vectors", "Cross product and area of parallelogram", "Vector equations of lines and planes"],
        "Matrices":            ["Matrix operations — add, subtract, multiply", "Determinant — 2x2 and 3x3", "Inverse of a matrix", "Solving linear systems using matrices", "Eigenvalues and eigenvectors basics"],
        "Probability":         ["Sample space and basic probability", "Addition and multiplication rules", "Conditional probability and Bayes theorem", "Permutations and combinations", "Binomial and normal distributions"],
        "Statistics":          ["Mean, median, mode and range", "Variance and standard deviation", "Correlation coefficient", "Linear regression line", "Hypothesis testing — z and t tests"],
    },
    "biology": {
        "Cell Biology":      ["Prokaryote vs eukaryote cell structure", "Cell organelles — nucleus, mitochondria, ER", "Cell membrane — fluid mosaic model", "Mitosis — PMAT stages", "Meiosis — stages and significance"],
        "Genetics":          ["Mendel's law of segregation", "Monohybrid and dihybrid cross — Punnett square", "Codominance and incomplete dominance", "Sex-linked inheritance — X-linked traits", "Chromosomal disorders — Down, Turner, Klinefelter"],
        "Molecular Biology": ["DNA double helix — Watson and Crick", "DNA replication — semiconservative", "Transcription — promoter to mRNA", "Translation — codons, tRNA, ribosomes", "Gene regulation — operon model"],
        "Human Physiology":  ["Digestive system — enzymes and absorption", "Circulatory system — heart chambers and blood flow", "Respiratory system — gas exchange in alveoli", "Excretory system — nephron and urine formation", "Nervous system — neuron structure and synapse"],
        "Plant Biology":     ["Plant tissue — meristematic and permanent", "Photosynthesis — light reactions in thylakoid", "Calvin cycle — CO2 fixation", "Transpiration and stomata", "Plant hormones — auxin, gibberellin, cytokinin"],
        "Ecology":           ["Ecosystem — biotic and abiotic components", "Food chain and food web", "Energy flow — 10% law", "Biogeochemical cycles — carbon and nitrogen", "Biodiversity — types and conservation methods"],
        "Evolution":         ["Darwin's theory — variation and natural selection", "Evidence — fossil record, comparative anatomy", "Speciation — allopatric and sympatric", "Human evolution — Homo sapiens timeline", "Hardy-Weinberg equilibrium"],
        "Biotechnology":     ["Recombinant DNA — restriction enzymes", "PCR — steps and applications", "Gel electrophoresis — separation by size", "CRISPR-Cas9 gene editing", "Applications — insulin, vaccines, GM crops"],
    },
    "history": {
        "Ancient History":          ["Prehistoric humans and stone age", "Indus Valley Civilization — cities and culture", "Vedic period — early kingdoms", "Mauryan Empire — Chandragupta and Ashoka", "Gupta Empire — golden age"],
        "Medieval History":         ["Delhi Sultanate — five dynasties", "Mughal Empire — Akbar's administration", "Mughal decline — Aurangzeb's policies", "Maratha Empire — Shivaji", "Vijayanagara and Bahmani kingdoms"],
        "Modern History":           ["European arrival — Portuguese and British", "British East India Company rule", "1857 revolt — causes, events, results", "Social reform movements — Ram Mohan Roy", "Early nationalism — INC formation 1885"],
        "Indian Independence":      ["Gandhi — non-cooperation movement 1920", "Civil disobedience — Salt March 1930", "Quit India movement 1942", "Partition of India — causes and impact", "Constitution making — Dr. Ambedkar"],
        "World Wars":               ["WWI — causes — MAIN acronym", "WWI — major battles and outcome", "WWII — causes — appeasement policy", "WWII — Holocaust and atomic bombs", "Post-war — UN formation and Cold War"],
        "Revision":                 ["Timeline of Indian history — ancient to modern", "Key personalities and their contributions", "Important dates and events", "Map-based questions — battles and empires", "Previous year question practice"],
    },
    "geography": {
        "Physical Geography": ["Earth's structure — crust, mantle, core", "Rocks — igneous, sedimentary, metamorphic", "Landforms — mountains, plateaus, plains", "Rivers — erosion, transportation, deposition", "Glaciers and coastal landforms"],
        "Human Geography":    ["Population distribution and density factors", "Migration — push and pull factors", "Urbanization — causes and problems", "Agriculture — types and crop patterns", "Industries — location factors"],
        "Indian Geography":   ["Physical features — Himalayas, Deccan, Plains", "Rivers — Ganga, Brahmaputra, peninsular", "Climate — monsoon mechanism", "Natural resources — coal, iron, petroleum", "Agriculture — Green Revolution"],
        "World Geography":    ["Continents and oceans overview", "Major mountain ranges and rivers", "Climate zones — equatorial to polar", "Natural vegetation — biomes", "Major countries — capitals and economies"],
        "Map Skills":         ["Latitude and longitude — locating places", "Time zones — IST and GMT", "Topographic maps — contour lines", "Scale — representative fraction", "Directions and compass bearings"],
        "Revision":           ["Map identification practice", "Fill in the blanks — key facts", "Compare regions and countries", "Current environmental issues", "Previous year questions"],
    },
    "economics": {
        "Microeconomics":    ["Demand — law and determinants", "Supply — law and determinants", "Market equilibrium — price mechanism", "Elasticity of demand — types and formula", "Consumer equilibrium — MU approach"],
        "Macroeconomics":    ["National income — GDP, GNP, NNP, NI", "Circular flow of income", "Consumption and investment functions", "Keynesian multiplier", "AD-AS model"],
        "Money & Banking":   ["Functions of money", "Money supply — M1, M2, M3", "Commercial bank — credit creation", "Central bank — RBI functions", "Monetary policy tools — CRR, SLR, Repo"],
        "Indian Economy":    ["Economic planning — Five Year Plans", "Poverty — causes and measures", "Unemployment — types and remedies", "GST and tax reforms", "Make in India and other schemes"],
        "International Trade":["Theory of comparative advantage", "Balance of payments — current and capital", "Exchange rates — fixed vs flexible", "WTO and trade agreements", "Foreign direct investment"],
        "Revision":          ["Key definitions and formulas", "Diagrams — demand, supply, IS-LM", "Numerical problems — national income", "Comparison — micro vs macro", "Previous year questions"],
    },
    "accountancy": {
        "Journal & Ledger":       ["Accounting equation and double entry", "Rules of debit and credit — DEAD CLIC", "Journal entries — simple and compound", "Ledger posting and balancing", "Trial balance preparation"],
        "Financial Statements":   ["Trading account — gross profit", "Profit and loss account — net profit", "Balance sheet — assets and liabilities", "Adjustments — prepaid, accrued, depreciation", "Rectification of errors"],
        "Partnership":            ["Partnership deed and capital accounts", "Profit sharing and interest on capital", "Admission — goodwill and revaluation", "Retirement — gaining ratio and settlement", "Dissolution — realisation account"],
        "Company Accounts":       ["Issue of shares at par, premium, discount", "Forfeiture and reissue of shares", "Issue of debentures — types", "Redemption of debentures", "Final accounts of a company"],
        "Ratio Analysis":         ["Liquidity — current and quick ratio", "Profitability — gross and net profit ratio", "Solvency — debt-equity ratio", "Activity — inventory and debtors turnover", "Interpret and compare ratios"],
        "Revision":               ["Journal entry practice — 20 entries", "Prepare trading and P&L account", "Balance sheet from trial balance", "Partnership numericals", "Previous year board questions"],
    },
}

# Full subject curriculum for when NO topics are selected
SUBJECT_CURRICULUM = {
    "python": [
        "Setup Python environment, print Hello World",
        "Variables, data types (int, float, str, bool)",
        "String operations and string methods",
        "Lists — creation, indexing, slicing",
        "List methods — append, remove, sort, reverse",
        "Tuples and Sets — differences and use cases",
        "Dictionaries — keys, values, iteration",
        "If/else conditions and comparison operators",
        "Loops — for loop with range and lists",
        "While loops and break/continue",
        "Functions — def, parameters, return values",
        "Default arguments and keyword arguments",
        "Lambda functions and map/filter",
        "File handling — read, write, append",
        "Exception handling — try/except/finally",
        "List comprehensions",
        "Modules and import system",
        "OOP — classes and objects",
        "OOP — inheritance and polymorphism",
        "OOP — encapsulation and dunder methods",
        "Popular libraries — os, sys, math, random",
        "Working with JSON data",
        "Regular expressions basics",
        "Recursion and recursive functions",
        "Practice: Build a calculator",
        "Practice: Build a to-do list app",
        "Practice: File-based student records system",
        "Revision: Data types and functions",
        "Revision: OOP concepts",
        "Mock test and full revision",
    ],
    "java": [
        "JDK setup, Hello World, main method structure",
        "Variables, data types, type casting",
        "Operators — arithmetic, relational, logical",
        "String class and string methods",
        "Scanner class for user input",
        "If/else, switch statements",
        "For loop, while loop, do-while loop",
        "Arrays — 1D declaration and iteration",
        "2D arrays and matrix operations",
        "Methods — declaration, parameters, return types",
        "Method overloading",
        "OOP — Classes and Objects",
        "Constructors and this keyword",
        "Inheritance and super keyword",
        "Method overriding and @Override",
        "Abstract classes and interfaces",
        "Polymorphism — compile time and runtime",
        "Encapsulation — getters and setters",
        "ArrayList and LinkedList",
        "HashMap and HashSet",
        "Exception handling — try/catch/finally",
        "Custom exceptions",
        "File I/O — FileReader and FileWriter",
        "Generics basics",
        "Threads and basic multithreading",
        "Lambda expressions (Java 8+)",
        "Streams API basics",
        "Practice: Build a bank account system",
        "Revision: OOP and Collections",
        "Mock test and full revision",
    ],
    "javascript": [
        "Variables — var, let, const differences",
        "Data types and typeof operator",
        "String methods and template literals",
        "Arrays and array methods",
        "Objects — creation, access, methods",
        "If/else, ternary operator",
        "Loops — for, while, for...of, for...in",
        "Functions — declaration vs expression",
        "Arrow functions",
        "Scope — global, local, block scope",
        "Closures and lexical scope",
        "DOM selection — getElementById, querySelector",
        "DOM manipulation — innerHTML, style, classList",
        "Event listeners — click, input, submit",
        "Forms and form validation",
        "Promises and async/await",
        "Fetch API and REST calls",
        "JSON parse and stringify",
        "ES6 — destructuring, spread, rest",
        "ES6 — modules, import/export",
        "Array methods — map, filter, reduce",
        "Error handling — try/catch",
        "Classes and OOP in JS",
        "Practice: Build a todo app",
        "Practice: Weather app using fetch",
        "Revision: Async concepts",
        "Revision: DOM and events",
        "Mock test and full revision",
    ],
    "mathematics": [
        "Number system — real, rational, irrational",
        "Algebra — polynomials and factoring",
        "Linear equations and inequalities",
        "Quadratic equations and discriminant",
        "Sequences and series — AP and GP",
        "Logarithms and exponentials",
        "Sets, relations and functions",
        "Trigonometry — ratios and identities",
        "Trigonometry — inverse functions",
        "Straight lines and coordinate geometry",
        "Circles — equations and properties",
        "Conic sections — parabola, ellipse, hyperbola",
        "Limits and continuity",
        "Differentiation — first principles",
        "Differentiation — chain, product, quotient rules",
        "Applications — maxima and minima",
        "Integration — basic rules and substitution",
        "Integration — by parts and partial fractions",
        "Definite integrals and area under curve",
        "Vectors — dot and cross product",
        "Matrices — operations and determinants",
        "Probability — basic and conditional",
        "Statistics — mean, median, mode, variance",
        "Practice: Mixed problem solving",
        "Revision: Calculus",
        "Mock test and full revision",
    ],
    "physics": [
        "Units, dimensions and significant figures",
        "Kinematics — equations of motion",
        "Newton's laws of motion",
        "Work, energy and power",
        "Conservation of momentum",
        "Rotational motion and torque",
        "Gravitation — Newton's law",
        "Simple harmonic motion",
        "Waves — transverse and longitudinal",
        "Thermodynamics — first and second law",
        "Electric charges and Coulomb's law",
        "Electric field and potential",
        "Capacitors",
        "Current, resistance and Ohm's law",
        "Kirchhoff's laws",
        "Magnetic field and force",
        "Electromagnetic induction",
        "Optics — reflection and refraction",
        "Lenses and mirrors",
        "Modern physics — photoelectric effect",
        "Revision: Mechanics",
        "Revision: Electromagnetism",
        "Mock test and full revision",
    ],
    "chemistry": [
        "Atomic structure and periodic table",
        "Chemical bonding — ionic and covalent",
        "States of matter and gas laws",
        "Thermochemistry — enthalpy",
        "Chemical equilibrium",
        "Acids, bases and pH",
        "Electrochemistry",
        "Chemical kinetics",
        "Organic chemistry — nomenclature",
        "Functional groups",
        "Reaction mechanisms",
        "Stoichiometry and mole concept",
        "Revision: Physical chemistry",
        "Revision: Organic chemistry",
        "Mock test and full revision",
    ],
    "biology": [
        "Cell structure and organelles",
        "Cell division — mitosis and meiosis",
        "Biomolecules and enzymes",
        "DNA structure and replication",
        "Genetics — Mendelian laws",
        "Evolution — Darwin's theory",
        "Human digestive system",
        "Human circulatory system",
        "Human respiratory system",
        "Nervous and endocrine system",
        "Photosynthesis",
        "Ecology and biodiversity",
        "Biotechnology basics",
        "Revision: Genetics and molecular biology",
        "Mock test and full revision",
    ],
    "data structures": [
        "Arrays and complexity analysis",
        "Linked lists — singly and doubly",
        "Stacks — implementation and applications",
        "Queues — types and implementation",
        "Trees — binary tree and BST",
        "Tree traversals",
        "Heap and priority queue",
        "Hashing and hash tables",
        "Graphs — BFS and DFS",
        "Shortest path algorithms",
        "Sorting algorithms",
        "Searching algorithms",
        "Practice: Implement all structures",
        "Mock test and full revision",
    ],
    "machine learning": [
        "NumPy and Pandas basics",
        "Data preprocessing",
        "Linear regression",
        "Logistic regression",
        "Decision trees and random forests",
        "SVM and KNN",
        "K-means clustering",
        "Neural networks basics",
        "Model evaluation metrics",
        "Hyperparameter tuning",
        "Practice: Classification project",
        "Practice: Regression project",
        "Mock test and full revision",
    ],
    "sql": [
        "CREATE TABLE and data types",
        "INSERT, UPDATE, DELETE",
        "SELECT and WHERE clause",
        "ORDER BY and LIMIT",
        "Aggregate functions",
        "GROUP BY and HAVING",
        "INNER JOIN",
        "LEFT and RIGHT JOIN",
        "Subqueries",
        "Views and indexes",
        "Stored procedures",
        "Normalization",
        "Practice: Library database",
        "Mock test and full revision",
    ],
    "react": [
        "JSX and functional components",
        "Props and state",
        "useState hook",
        "useEffect hook",
        "Event handling",
        "Lists and conditional rendering",
        "Forms and controlled components",
        "React Router",
        "useContext",
        "useReducer",
        "Custom hooks",
        "API calls with fetch/axios",
        "Redux basics",
        "Practice: Full CRUD app",
        "Mock test and full revision",
    ],
    "web development": [
        "HTML — structure and forms",
        "CSS — flexbox and grid",
        "CSS — responsive design",
        "JavaScript — DOM and events",
        "JavaScript — fetch API",
        "Git basics",
        "Node.js and Express",
        "REST API design",
        "MongoDB basics",
        "Authentication — JWT",
        "React basics",
        "Deployment",
        "Practice: Full stack todo app",
        "Mock test and full revision",
    ],
}

FALLBACK_STEPS = [
    "Read through all notes and textbook once",
    "Highlight and summarize key points",
    "Create flashcards for important terms",
    "Solve past exam questions",
    "Test yourself with practice problems",
    "Make a one-page summary sheet",
    "Review weak areas identified",
    "Final quick revision",
]


def get_concentration_factor(days_until_exam: int) -> float:
    for threshold, factor in CONCENTRATION_FACTORS:
        if days_until_exam <= threshold:
            return factor
    return 1.0


def calculate_priority(subject) -> float:
    days_left = subject.days_left
    if not days_left or days_left <= 0:
        return 0.0
    return round(
        (10 / days_left)
        + (subject.difficulty * 2)
        + ((100 - subject.syllabus_completion) / 10),
        4
    )


def _compute_subject_weights(subjects) -> dict:
    return {
        s.id: DIFFICULTY_MULTIPLIERS.get(s.difficulty, 1.0)
               * s.daily_hours_available
        for s in subjects
        if s.days_left > 0
    }


def _assign_time_slots(subjects_with_hours: list, day_offset: int) -> list:
    sorted_subjects = sorted(
        subjects_with_hours,
        key=lambda x: calculate_priority(x[0]),
        reverse=True
    )
    assignments = []
    slot_index  = 0
    for subject, hours in sorted_subjects:
        if slot_index >= len(STUDY_SLOTS):
            slot_index = 0
        start    = STUDY_SLOTS[slot_index][0]
        start_dt = datetime.combine(date.today(), start)
        end_dt   = start_dt + timedelta(hours=hours)
        end      = end_dt.time()
        if end_dt.date() > date.today():
            end = time(23, 59)
        assignments.append((subject, start, end, hours))
        slot_index += 1
    return assignments


def _get_topic_steps(subject_key: str, selected_topics: list, day_offset: int) -> list:
    """
    Given selected topics, build an ordered list of steps across all topics
    and return today's 4 steps based on day_offset progression.
    """
    topic_map = None
    for k in TOPIC_STEPS:
        if k in subject_key or subject_key in k:
            topic_map = TOPIC_STEPS[k]
            break

    if not topic_map or not selected_topics:
        return None

    # Build master step list in topic order
    all_steps = []
    for topic in selected_topics:
        steps = topic_map.get(topic, [])
        for step in steps:
            all_steps.append(f"[{topic}] {step}")

    if not all_steps:
        return None

    # Progress through steps day by day — 4 steps per day
    total   = len(all_steps)
    start_i = (day_offset * 4) % total
    end_i   = min(start_i + 4, total)
    result  = all_steps[start_i:end_i]

    # Wrap if near end
    if len(result) < 2:
        result = all_steps[-4:]

    return result


def get_study_approach(subject_name: str, difficulty: int,
                       day_offset: int = 0, selected_topics: list = None) -> dict:
    difficulty_tips = {
        1: {"approach": "Light Review",   "technique": "Spaced repetition + quick quizzes"},
        2: {"approach": "Active Learning","technique": "Pomodoro (25min study / 5min break)"},
        3: {"approach": "Deep Work",      "technique": "Feynman technique + practice problems"},
    }

    name_lower = subject_name.lower().strip()
    tips       = difficulty_tips.get(difficulty, difficulty_tips[2])

    # ── 1. Topic-specific steps (highest priority) ────
    if selected_topics and len(selected_topics) > 0:
        topic_steps = _get_topic_steps(name_lower, selected_topics, day_offset)
        if topic_steps:
            return {
                "approach":  tips["approach"],
                "technique": tips["technique"],
                "steps":     topic_steps,
            }

    # ── 2. Full curriculum steps (no topics selected) ─
    curriculum = None
    for key, steps in SUBJECT_CURRICULUM.items():
        if key in name_lower or name_lower in key:
            curriculum = steps
            break

    if curriculum:
        total       = len(curriculum)
        start_i     = (day_offset * 2) % total
        end_i       = min(start_i + 4, total)
        today_steps = curriculum[start_i:end_i]
        if len(today_steps) < 2:
            today_steps = curriculum[-4:]
        return {"approach": tips["approach"], "technique": tips["technique"], "steps": today_steps}

    # ── 3. Generic fallback ───────────────────────────
    if any(k in name_lower for k in ["math", "calculus", "algebra", "statistics", "trigonometry"]):
        today_steps = ["Review theory and key formulas", "Solve 5 warm-up problems", "Attempt past exam questions", "Identify weak areas and re-study"]
    elif any(k in name_lower for k in ["physics", "chemistry", "science"]):
        today_steps = ["Study diagrams and processes", "Memorize key formulas", "Solve numerical problems", "Revise with chapter summary"]
    elif any(k in name_lower for k in ["history", "geography", "civics", "political"]):
        today_steps = ["Create timeline of key events", "Make mind maps for chapters", "Write summaries in own words", "Answer previous year questions"]
    elif any(k in name_lower for k in ["english", "language", "literature", "writing"]):
        today_steps = ["Read chapter/passage carefully", "Note key themes and vocabulary", "Practice grammar exercises", "Write one practice essay"]
    elif any(k in name_lower for k in ["law", "legal", "constitution"]):
        today_steps = ["Read the relevant act/section", "Note key definitions", "Study landmark case judgments", "Solve hypothetical problems"]
    elif any(k in name_lower for k in ["account", "finance", "commerce"]):
        today_steps = ["Study the accounting concept", "Practice journal entries", "Prepare ledger and trial balance", "Solve past exam numericals"]
    else:
        idx = (day_offset * 2) % len(FALLBACK_STEPS)
        today_steps = FALLBACK_STEPS[idx:idx+4] or FALLBACK_STEPS[:4]

    return {"approach": tips["approach"], "technique": tips["technique"], "steps": today_steps}


def generate_timetable(user) -> dict:
    subjects = list(user.subjects.select_related().all())
    StudySession.objects.filter(subject__user=user).delete()

    if not subjects:
        return {"sessions_created": 0, "skipped_subjects": [], "timetable": []}

    skipped        = [s.name for s in subjects if s.is_exam_passed]
    valid_subjects = [s for s in subjects if not s.is_exam_passed]

    if not valid_subjects:
        return {"sessions_created": 0, "skipped_subjects": skipped, "timetable": []}

    max_days = max(s.days_left for s in valid_subjects)
    if max_days <= 0:
        return {"sessions_created": 0, "skipped_subjects": skipped, "timetable": []}

    sessions_to_create = []
    timetable_preview  = []
    today = date.today()

    for day_offset in range(max_days):
        current_date    = today + timedelta(days=day_offset)
        active_subjects = [s for s in valid_subjects if s.days_left > day_offset]
        if not active_subjects:
            continue

        daily_weights = _compute_subject_weights(active_subjects)
        total_weight  = sum(daily_weights.values())

        day_subjects = []
        for subject in active_subjects:
            weight          = daily_weights.get(subject.id, 0)
            base_hours      = (weight / total_weight * subject.daily_hours_available
                               if total_weight else
                               subject.daily_hours_available / len(active_subjects))
            days_until_exam = subject.days_left - day_offset
            final_hours     = round(base_hours * get_concentration_factor(days_until_exam), 2)
            day_subjects.append((subject, final_hours))

        assignments = _assign_time_slots(day_subjects, day_offset)

        for subject, start_time, end_time, hours in assignments:
            sessions_to_create.append(
                StudySession(
                    subject=subject,
                    date=current_date,
                    hours_allocated=hours,
                    notes=f"{start_time.strftime('%I:%M %p')} – {end_time.strftime('%I:%M %p')}",
                )
            )

            if day_offset < 14:
                # Pass selected_topics from subject model
                approach = get_study_approach(
                    subject.name,
                    subject.difficulty,
                    day_offset,
                    selected_topics=subject.selected_topics or [],
                )
                timetable_preview.append({
                    "date":       current_date.strftime("%d %b %Y"),
                    "day":        current_date.strftime("%A"),
                    "subject":    subject.name,
                    "priority":   subject.priority_label,
                    "days_left":  subject.days_left - day_offset,
                    "start_time": start_time.strftime("%I:%M %p"),
                    "end_time":   end_time.strftime("%I:%M %p"),
                    "hours":      hours,
                    "approach":   approach["approach"],
                    "technique":  approach["technique"],
                    "steps":      approach["steps"],
                    "difficulty": subject.difficulty,
                    "topics":     subject.selected_topics or [],
                })

    StudySession.objects.bulk_create(sessions_to_create)

    return {
        "sessions_created": len(sessions_to_create),
        "skipped_subjects": skipped,
        "timetable":        timetable_preview,
    }