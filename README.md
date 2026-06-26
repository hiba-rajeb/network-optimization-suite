




# Network Optimization Algorithms 🚀

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)
[![NetworkX](https://img.shields.io/badge/NetworkX-Latest-green)](https://networkx.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-orange)](https://matplotlib.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive desktop application for learning and visualizing **graph theory** and **network optimization algorithms**. Built with Python, Tkinter, and NetworkX for educational and research purposes.

## 📸 Screenshots

### Main Dashboard
*The central hub for accessing all algorithms with network configuration options*

![Main Dashboard](screenshots/main_dashboard.png)
> **Note:** Take screenshot showing the main window with algorithm buttons

### Dijkstra Algorithm - Shortest Path
*Interactive shortest path calculation with real-time visualization*

![Dijkstra Algorithm](screenshots/dijkstra_algorithm.png)
> **Note:** Screenshot of Dijkstra interface with calculated path and graph

### Ford-Fulkerson - Maximum Flow (Directed Graph)
*Maximum flow calculation with oriented graphs and capacity visualization*

![Ford-Fulkerson Flow](screenshots/ford_fulkerson_flow.png)
> **Note:** Screenshot showing directed graph with arrows and flow values

### Bellman-Ford - Negative Weights Support
*Shortest path algorithm supporting negative weights with cycle detection*

![Bellman-Ford Algorithm](screenshots/bellman_ford_algorithm.png)
> **Note:** Screenshot of Bellman-Ford with directed graph visualization

### Welsh-Powell Graph Coloring
*Graph coloring algorithm with color-coded node visualization*

![Welsh-Powell Coloring](screenshots/welsh_powell_coloring.png)
> **Note:** Screenshot showing colored graph with different node colors

### Prim/Kruskal - Minimum Spanning Tree
*MST algorithms with highlighted spanning tree edges*

![MST Algorithms](screenshots/mst_algorithms.png)
> **Note:** Screenshot of MST with highlighted green edges

## ✨ Features

### 🎯 **7 Classical Algorithms Implemented:**

| Algorithm | Type | Features |
|-----------|------|----------|
| **Dijkstra** | Shortest Path | Non-negative weights, optimal paths |
| **Bellman-Ford** | Shortest Path | Negative weights, cycle detection |
| **Ford-Fulkerson** | Maximum Flow | Capacity constraints, augmenting paths |
| **Prim** | Minimum Spanning Tree | Greedy approach, connected components |
| **Kruskal** | Minimum Spanning Tree | Union-find, edge sorting |
| **Welsh-Powell** | Graph Coloring | Vertex coloring, chromatic number |
| **Nord-Ouest** | Transportation | Linear programming, supply-demand |

### 🎨 **Advanced Visualization:**
- ✅ **Real-time graph rendering** with matplotlib integration
- ✅ **Directed graphs** with arrows positioned at edge midpoints
- ✅ **Color-coded results** (paths, flows, spanning trees, colorations)
- ✅ **Interactive zoom & pan** functionality
- ✅ **Dynamic network reconfiguration** (1-100 nodes, 1-100% density)
- ✅ **Professional graph layouts** with edge labels and legends

### 🖥️ **Modern User Interface:**
- ✅ Clean, **scrollable interfaces** for all algorithm windows
- ✅ **Entry field validation** with real-time feedback
- ✅ **Configuration panels** for network customization
- ✅ **Step-by-step result display** with detailed metrics
- ✅ **Error handling** with informative messages
- ✅ **Responsive design** with resizable windows

## 🛠️ **Technical Stack:**

```python
🐍 Python 3.7+        # Core language
🖼️  Tkinter            # Native GUI framework  
📊 NetworkX           # Graph algorithms & data structures
📈 Matplotlib         # Advanced graph visualization
🔢 NumPy              # Mathematical computations
📝 Logging            # Application monitoring
```

## 📋 **Installation Requirements:**

### System Requirements:
- **Python 3.7 or higher**
- **Operating System:** Windows, macOS, Linux
- **Memory:** 512MB RAM minimum
- **Storage:** 100MB free space

### Python Dependencies:
```txt
networkx>=2.6
matplotlib>=3.5.0
numpy>=1.21.0
```

## 🚀 **Quick Start Guide:**

### 1. Clone the Repository:
```bash
git clone https://github.com/Ayoub-glitsh/network-optimization-algorithms.git
cd network-optimization-algorithms
```

### 2. Install Dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Or install manually
pip install networkx matplotlib numpy
```

### 3. Run the Application:
```bash
python app/main.py
```

### 4. Start Exploring:
1. **Configure your network** → Set nodes (1-100) and density (1-100%)
2. **Choose an algorithm** → Click on any algorithm button
3. **Set parameters** → Select source/destination nodes
4. **Calculate & visualize** → View results and interactive graphs

## 📁 **Project Architecture:**

```
network-optimization-algorithms/
├── 📁 app/                     # Main application directory
│   ├── 📁 algorithms/          # Algorithm implementations
│   │   ├── 🐍 dijkstra.py     # Shortest path (non-negative)
│   │   ├── 🐍 bellman_ford.py # Shortest path (negative weights)
│   │   ├── 🐍 ford_fulkerson.py # Maximum flow
│   │   ├── 🐍 prim.py         # MST (vertex-based)
│   │   ├── 🐍 kruskal.py      # MST (edge-based)
│   │   ├── 🐍 welsh_powell.py # Graph coloring
│   │   └── 🐍 nord_ouest.py   # Transportation method
│   ├── 📁 models/             # Data models & structures
│   │   └── 🐍 reseau.py       # Network/Graph model with oriented support
│   ├── 📁 views/              # User interface components
│   │   ├── 🐍 main_window.py  # Main dashboard
│   │   ├── 🐍 graph_view.py   # Graph visualization engine
│   │   ├── 🐍 theme.py        # UI styling & components
│   │   └── 🐍 *_view.py       # Algorithm-specific interfaces
│   ├── 📁 services/           # Utility services
│   │   └── 🐍 logger.py       # Application logging
│   └── 🐍 main.py            # Application entry point
├── 📁 screenshots/            # Application screenshots
├── 📄 README.md              # This documentation
├── 📄 requirements.txt       # Python dependencies
├── 📄 .gitignore            # Git ignore rules
└── 📄 build.bat             # Build script for Windows
```

## 🎮 **Detailed Usage Guide:**

### **Basic Workflow:**
1. **Launch Application** → `python app/main.py`
2. **Network Configuration:**
   - Set **number of nodes** (1-100)
   - Adjust **graph density** (1-100%)
   - Click **"Apply Configuration"**
3. **Algorithm Selection:**
   - Choose from 7 available algorithms
   - Each opens a dedicated interface
4. **Parameter Setup:**
   - Select **source & destination** nodes
   - Configure algorithm-specific options
5. **Execute & Visualize:**
   - Click **"Calculate"** to run algorithm
   - Use **"View Graph"** for visualization
   - Analyze results and metrics

### **Advanced Features:**
- **Dynamic Reconfiguration:** Change network parameters without restarting
- **Multiple Views:** Switch between complete graph and result visualization
- **Export Options:** Save configurations and results
- **Error Recovery:** Robust error handling with helpful messages

## 🔬 **Algorithm Details & Complexity:**

### **Shortest Path Algorithms:**

#### **Dijkstra's Algorithm**
- **Time Complexity:** O((V + E) log V)
- **Space Complexity:** O(V)
- **Use Case:** Non-negative edge weights
- **Features:** Priority queue implementation, optimal substructure

#### **Bellman-Ford Algorithm**
- **Time Complexity:** O(VE)
- **Space Complexity:** O(V)
- **Use Case:** Negative edge weights, cycle detection
- **Features:** Relaxation technique, negative cycle detection

### **Maximum Flow:**

#### **Ford-Fulkerson Algorithm**
- **Time Complexity:** O(Ef), where f is maximum flow
- **Space Complexity:** O(V + E)
- **Use Case:** Network flow optimization, capacity constraints
- **Features:** Residual graph, augmenting paths, BFS implementation

### **Minimum Spanning Tree:**

#### **Prim's Algorithm**
- **Time Complexity:** O((V + E) log V)
- **Space Complexity:** O(V)
- **Approach:** Vertex-based, greedy selection

#### **Kruskal's Algorithm**
- **Time Complexity:** O(E log E)
- **Space Complexity:** O(V)
- **Approach:** Edge-based, union-find data structure

### **Graph Coloring:**

#### **Welsh-Powell Algorithm**
- **Time Complexity:** O(V²)
- **Space Complexity:** O(V)
- **Features:** Degree-based ordering, greedy coloring

### **Transportation:**

#### **Nord-Ouest Method**
- **Time Complexity:** O(mn)
- **Space Complexity:** O(mn)
- **Features:** Supply-demand balancing, northwest corner rule

## 🎨 **Visualization Features:**

### **Graph Rendering:**
- **Node Layouts:** Spring, circular, random positioning
- **Edge Styling:** Different colors, widths, and styles
- **Label Management:** Node IDs, edge weights, capacities
- **Interactive Controls:** Zoom, pan, reset view

### **Algorithm-Specific Visualization:**
- **Path Highlighting:** Yellow paths for shortest routes
- **Flow Visualization:** Capacity and flow values on edges
- **Tree Highlighting:** Green edges for spanning trees
- **Color Coding:** Multi-color nodes for graph coloring
- **Directed Graphs:** Arrow indicators for flow direction

## 📚 **Educational Applications:**

### **Perfect for:**
- 🎓 **Computer Science Students:** Learning graph algorithms
- 👨‍🏫 **Educators:** Demonstrating algorithmic concepts
- 🔬 **Researchers:** Prototyping network optimization solutions
- 💼 **Professionals:** Visualizing network problems
- 📖 **Self-learners:** Understanding graph theory concepts

### **Learning Benefits:**
- **Visual Learning:** See algorithms in action
- **Interactive Exploration:** Experiment with different parameters
- **Comparative Analysis:** Compare algorithm performance
- **Real-world Applications:** Understand practical use cases

## 🤝 **Contributing:**

We welcome contributions from the community! Here's how you can help:

### **Ways to Contribute:**
- 🐛 **Bug Reports:** Found an issue? Open an issue on GitHub
- 💡 **Feature Requests:** Have an idea? Share it with us
- 🔧 **Code Contributions:** Submit pull requests for improvements
- 📝 **Documentation:** Help improve documentation and examples
- 🎨 **UI/UX Improvements:** Enhance the user interface

### **Development Setup:**
```bash
# Fork the repository
git clone https://github.com/yourusername/network-optimization-algorithms.git
cd network-optimization-algorithms

# Create development branch
git checkout -b feature/your-feature-name

# Make changes and test
python app/main.py

# Submit pull request
git push origin feature/your-feature-name
```

## 📄 **License:**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Ayoub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 **Acknowledgments:**

### **Special Thanks:**
- **NetworkX Community** - Excellent graph library
- **Matplotlib Team** - Powerful visualization tools
- **Python Core Team** - Amazing programming language
- **Tkinter Developers** - Reliable GUI framework
- **Open Source Community** - Inspiration and support

### **References & Resources:**
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Graph Theory Algorithms](https://en.wikipedia.org/wiki/Graph_theory)
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms-third-edition)

## 🌟 **Star History:**

[![Star History Chart](https://api.star-history.com/svg?repos=Ayoub-glitsh/network-optimization-algorithms&type=Date)](https://star-history.com/#Ayoub-glitsh/network-optimization-algorithms&Date)

## 📞 **Support & Contact:**

- 🐙 **GitHub Issues:** [Report bugs or request features](https://github.com/Ayoub-glitsh/network-optimization-algorithms/issues)
- 📧 **Email:** [Contact for questions or collaboration](mailto:your-email@example.com)
- 💬 **Discussions:** [Join community discussions](https://github.com/Ayoub-glitsh/network-optimization-algorithms/discussions)

---

<div align="center">

**⭐ Star this repository if you found it helpful! ⭐**

**Made with ❤️ for the graph theory and algorithms community**

[**🚀 Get Started**](https://github.com/Ayoub-glitsh/network-optimization-algorithms/archive/main.zip) • [**📚 Documentation**](#-detailed-usage-guide) • [**🐛 Report Bug**](https://github.com/Ayoub-glitsh/network-optimization-algorithms/issues) • [**💡 Request Feature**](https://github.com/Ayoub-glitsh/network-optimization-algorithms/issues)

</div>

---

## 🔄 **Version History:**

### v1.0.0 (Initial Release)
- ✅ 7 graph algorithms implemented
- ✅ Interactive GUI with Tkinter
- ✅ Real-time graph visualization  
- ✅ Directed graph support with arrows
- ✅ Dynamic network configuration
- ✅ Educational documentation

### Upcoming Features:
- 🔮 **v1.1.0:** Additional algorithms (A*, Floyd-Warshall)
- 🔮 **v1.2.0:** Export functionality (PNG, PDF, CSV)
- 🔮 **v1.3.0:** Algorithm animation and step-by-step execution
- 🔮 **v2.0.0:** Web-based version with modern UI

---

**Happy Graph Exploring! 🌐✨**
