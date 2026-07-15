# Building Dimer CAS States, Symmetries, and CI-Vectors from Monomer Orbitals

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0)

> **Author**: [Judith M. Leson](https://orcid.org/0009-0002-5627-2673)  
> **Repository**: [https://github.com/jmleson/building_dimer_from_monomer_symmetries_and_civectors](https://github.com/jmleson/building_dimer_from_monomer_symmetries_and_civectors)  
> **Related Work**: Dissertation: *A Quantum-Chemical Analysis of Long-Range Dimer Interactions Arising From Triplet Excited States of Monocyclic Aromatics* (University of Duisburg-Essen, 2026)  
> **Data DOI**: [10.71955/DUEDATA-2026-MR4YY63J](https://doi.org/10.71955/DUEDATA-2026-MR4YY63J)

---

## 📌 Overview

This repository provides **automated Python code** to derive **dimer states, symmetries, and CI vectors** from **monomer orbital occupation and symmetry information**. This enables the correlation between monomer and dimer **Complete Active Space (CAS)** excited state calculations.

It is designed for **stacked aromatic dimers** such as:

|                     | D₆h (approx. D₂h)                                                                                                                                         | C₂v                        | D₂h                                                                                                                                                                |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Exemplary Molecule: | **Benzene (C₆H₆)**                                                                                                                                        | **Chlorobenzene (C₆H₅Cl)**                                                                                                                       | **Rotated Chlorobenzene (C₆H₅Cl)**                                                                                                                                         |
| Vizualization:      | <div style="text-align: center;"><img src="C6H6-x2-abstandZ100.png" alt="Stacked benzene dimer (D₂h symmetry)" style="width: 300px; height: auto;"></div> | <div style="text-align: center;"><img src="C6H5Cl-x2.png" alt="Chlorobenzene dimer (C₂v symmetry)" style="width: 300px; height: auto;"></div> | <br/><div style="text-align: center;"><img src="C6H5Cl_rotated-x2.png" alt="Rotated chlorobenzene dimer (D₂h symmetry)" style="width: 300px; height: auto;"></div> |


The code systematically constructs **dimer configurations** by combining **monomer states** (ground, triplet, quintet state(s)) and determines:
- The **symmetry of the resulting dimer state**
- The **set of CI vectors** (Slater determinants) included in the CAS(4,4) wavefunction
- The **mapping between monomer and dimer states**

This is particularly useful for **interpreting CAS calculations** of excited states in dimers, where the physical meaning of the CI vectors is not immediately obvious.

> ✅ The output is **traceable, step-by-step, and human-readable**, and documents important steps in the set-up of the thesis *"A Quantum-Chemical Analysis of Long-Range Dimer Interactions Arising From Triplet Excited States of Monocyclic Aromatics"*

---

## 🎯 Why This Matters

Usually, quantum-chemical CAS calculations on dimers produce a lot CI vectors. 
Without a clear mapping to mehr übersichtliche monomer states, it becomes difficult to:
- Assign physical meaning to excited states
- Understand how monomer excitations combine
- Validate the correctness of the active space

This tool **bridges the gap** between monomer properties and dimer wavefunctions, that happens un-nachvollziehbar in most quantum chemistry programs, and instead gives a **transparent, interpretable, and traceable ** CAS space analysis.

---

## ✅ Key Features

- **Automated derivation** of dimer state symmetries from monomer orbital symmetries and occupations
- **Dimer CI vector generation** based on linear combinations of monomer states and their CI vectors
- **Support for multiple point groups**, enabling different molecular systems:
  - D₂h (e.g., benzene)
  - C₂v (e.g., chlorobenzene)
  - C₂h (e.g., rotated chlorobenzene)
- **Traceable, Step-by-step output** with full derivations
- **Compact and detailed LaTeX modes** for different use cases
- **Human-readable derivations in compiled PDFs** showing the intermediate steps
- **Enabled Comparison to Molpro Output Files** by transformations for equation formats

---

## 🛠️ How It Works

### Core Idea

A dimer state is built from **two monomer states** ( both in ground state or both excited). The symmetry of the dimer state is determined by building all **linear combinations** and finding the symmetry of the resulting **determinants**.
We note, that simply building the direcct product from monomer state symmetries fails to reproduce the true dimer state symmetries. An ausmultiplizireen ist nötig. 

The code:
1. Starts from the monomer orbital symmetries and CI vectors for different states
2. Enumerates all possible combinations of monomer states, that build a doubly excited dimer state 
3. Multiplies out the CI vector combinations to independent determinants/summanden 
4. Generates the corresponding CI vectors
5. Computes the resulting symmetries for determinants and states 
6. Summarizes the results in a LaTeX file

> ✅ The result is a **clear, traceable map** from monomer states to dimer states.

---
### Example: Benzene Dimer 
As an example, we consider benzene.
As quantum chemcial programs typically dont enable D6h calculation, we perform our considerations in the subgroup D2h. 


Considering HOMO-LUMO excitations, there are 4 possible triplet excited states, and one 
For a CAS(4,4) calculation on two benzene monomers:
\[S = 
 \quad + \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ; 
 \draw[<-, thick] (0.15, -0.85) -- (0.15, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ; 
 \draw[<-, thick] (1.15, -0.85) -- (1.15, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;;
\end{tikzpicture}\right) 
 \quad = \left|\underbrace{(b_{3g}^{\mathsf{l}})^{2}(b_{2g}^{\mathsf{l}})^{2}(b_{1u}^{\mathsf{l}})^{0}(a_{u}^{\mathsf{l}})^{0}}_{a_{g}}\right|\]
$$Q = 
 \quad + \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;\draw[->, thick] (0.35, -0.25) -- (0.35, 0.25) ;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;\draw[->, thick] (1.35, -0.25) -- (1.35, 0.25) ;
\end{tikzpicture}\right) 
 \quad = \left|\underbrace{(b_{3g}^{\mathsf{l}})^{1}(b_{2g}^{\mathsf{l}})^{1}(b_{1u}^{\mathsf{l}})^{1}(a_{u}^{\mathsf{l}})^{1}}_{a_{g}}\right|\]
\[i^3 b_{2u} = 
 \quad + \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ; 
 \draw[<-, thick] (0.15, -0.85) -- (0.15, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;\draw[->, thick] (0.35, -0.25) -- (0.35, 0.25) ;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;;
\end{tikzpicture}\right) 
- \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ; 
 \draw[<-, thick] (1.15, -0.85) -- (1.15, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;\draw[->, thick] (1.35, -0.25) -- (1.35, 0.25) ;
\end{tikzpicture}\right) 
 \quad = \left|\underbrace{(b_{3g}^{\mathsf{l}})^{1}(b_{2g}^{\mathsf{l}})^{2}(b_{1u}^{\mathsf{l}})^{1}(a_{u}^{\mathsf{l}})^{0}}_{b_{2u}}\right| - \left|\underbrace{(b_{3g}^{\mathsf{l}})^{2}(b_{2g}^{\mathsf{l}})^{1}(b_{1u}^{\mathsf{l}})^{0}(a_{u}^{\mathsf{l}})^{1}}_{b_{2u}}\right|\]
\[e^3 b_{2u} = 
 \quad + \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ; 
 \draw[<-, thick] (0.15, -0.85) -- (0.15, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;\draw[->, thick] (0.35, -0.25) -- (0.35, 0.25) ;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;;
\end{tikzpicture}\right) 
+ \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ; 
 \draw[<-, thick] (1.15, -0.85) -- (1.15, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;\draw[->, thick] (1.35, -0.25) -- (1.35, 0.25) ;
\end{tikzpicture}\right) 
 \quad = \left|\underbrace{(b_{3g}^{\mathsf{l}})^{1}(b_{2g}^{\mathsf{l}})^{2}(b_{1u}^{\mathsf{l}})^{1}(a_{u}^{\mathsf{l}})^{0}}_{b_{2u}}\right| + \left|\underbrace{(b_{3g}^{\mathsf{l}})^{2}(b_{2g}^{\mathsf{l}})^{1}(b_{1u}^{\mathsf{l}})^{0}(a_{u}^{\mathsf{l}})^{1}}_{b_{2u}}\right|$$
$$e^3 b_{3u} = 
 \quad + \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ; 
 \draw[<-, thick] (1.15, -0.85) -- (1.15, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;\draw[->, thick] (0.35, -0.25) -- (0.35, 0.25) ;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;;
\end{tikzpicture}\right) 
- \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ; 
 \draw[<-, thick] (0.15, -0.85) -- (0.15, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;\draw[->, thick] (1.35, -0.25) -- (1.35, 0.25) ;
\end{tikzpicture}\right) 
 \quad = \left|\underbrace{(b_{3g}^{\mathsf{l}})^{2}(b_{2g}^{\mathsf{l}})^{1}(b_{1u}^{\mathsf{l}})^{1}(a_{u}^{\mathsf{l}})^{0}}_{b_{3u}}\right| - \left|\underbrace{(b_{3g}^{\mathsf{l}})^{1}(b_{2g}^{\mathsf{l}})^{2}(b_{1u}^{\mathsf{l}})^{0}(a_{u}^{\mathsf{l}})^{1}}_{b_{3u}}\right|\]
\[i^3 b_{3u} = 
 \quad + \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ; 
 \draw[<-, thick] (1.15, -0.85) -- (1.15, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;\draw[->, thick] (0.35, -0.25) -- (0.35, 0.25) ;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;;
\end{tikzpicture}\right) 
+ \left(\begin{tikzpicture}[baseline={(current bounding box.center)}]
% lower MOs:
\draw[thick] (0,-0.6) -- (0.5,-0.6)%node[pos=0, left] {$b_{2g}$}
;\draw[->, thick] (0.35, -0.85) -- (0.35, -0.35) ; 
 \draw[<-, thick] (0.15, -0.85) -- (0.15, -0.35) ;\draw[thick] (1,-0.6) -- (1.5,-0.6)%node[pos=1, right] {$b_{3g}$}
;\draw[->, thick] (1.35, -0.85) -- (1.35, -0.35) ;
% upper MOs:
\draw[thick] (0,0) -- (0.5,0)%node[pos=0, left] {$b_{1u}$}
;;\draw[thick] (1,0) -- (1.5,0)%node[pos=1, right] {$a_{u}$}
;\draw[->, thick] (1.35, -0.25) -- (1.35, 0.25) ;
\end{tikzpicture}\right) 
 \quad = \left|\underbrace{(b_{3g}^{\mathsf{l}})^{2}(b_{2g}^{\mathsf{l}})^{1}(b_{1u}^{\mathsf{l}})^{1}(a_{u}^{\mathsf{l}})^{0}}_{b_{3u}}\right| + \left|\underbrace{(b_{3g}^{\mathsf{l}})^{1}(b_{2g}^{\mathsf{l}})^{2}(b_{1u}^{\mathsf{l}})^{0}(a_{u}^{\mathsf{l}})^{1}}_{b_{3u}}\right|$$


---

## 🔧 How to Use
### 📂 Structure
- `requirements.txt`: Needed python libraries
- `src`: Folder for source files
- `src/run.py`: Main script that generates correlations between monomer and dimer states for C6H6, C6H5Cl, and C6H5Cl rotated
- `resulting_tex_files/`: Folder for LaTeX compilation files
- `resulting_tex_files/run.sh`: Compiles `.tex` files into PDFs (output in `resulting_tex_files/build/`)


### 📦 Dependencies

This project requires:
- `itertools` 
- `re`
- `unittest` 

Install with:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


### 💻 Running the Code
Exemplary use of the code is given in `src/run.py` for different molecular systems.

In general, the results of a different order for a tensor can be gained by running: 
```python
tikz = get_summarizing_latex_file(Molecule.C6H6, ordering=order, detailed=False)
```

The parameter ```detailed``` determines whether the generated LaTeX file includes a detailed derivation or omits some steps to get a schlankere pdf version. 