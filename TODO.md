좋아. 지금까지 만든 Ark V0 아키텍처와 앞으로 해야 할 일들을 정리된 로드맵 형태로 정리해보자.

⸻

🔹 Ark V0 설계 아키텍처

1. 핵심 계층

User Code
   ↓
Project / Model (API)
   ↓
IR (Entity list + Dependency edges)
   ↓
SimpleSolver (minimal deterministic)
   ↓
Resolved IR (x, y, z 계산)
   ↓
Compiler / OpenSCAD lowering
   ↓
Output file (.scad)


⸻

2. 핵심 모듈 구조

src/ark/
├── __init__.py          # Public API: Model
├── entity.py            # Entity 정의 (Cube, semantic, source info)
├── model.py             # Model + add_cube/add_top_of + compile
├── solver.py            # SimpleSolver: top_of, align_x, etc.

tests/
├── test_entity.py       # Entity 생성 및 repr 테스트
├── test_model.py        # Model 단순 compile, duplicate ID, hierarchy, semantic, dependency, constraint 테스트
├── test_solver.py       # SimpleSolver 동작 확인, top_of, compile 결과 검증


⸻

3. 핵심 원칙 (Ark 4대 원칙)
	1.	Hierarchy: Structure / parent-child 관계 → future: structure tree, nested groups
	2.	Semantic: #Public, #Private 등 태그 → LLM이 의미 기반 수정 가능
	3.	Dependency: top_of, align_x, align_y 등 → solver에서 결정적 처리
	4.	Constraints: dimension, negative values 등 → compile()에서 오류로 보고

⸻

4. 현재 구현 상태 (V0)
	•	Entity 정의 (entity.py)
	•	Model 최소 skeleton (model.py)
	•	SimpleSolver 최소 top_of 구현 (solver.py)
	•	compile() → OpenSCAD 출력 가능
	•	TDD 테스트:
	•	Entity 생성
	•	단일 Cube compile
	•	top_of dependency 처리
	•	중복 ID / 음수 dimension 감지
	•	4대 원칙 테스트 placeholder 포함

⸻

🔹 앞으로 해야 할 일

A. Model 기능 확장
	1.	add_cube() → compile() 단계에서 중복 ID / invalid dimension 오류 처리 (LLM-friendly)
	2.	Dependency 확장
	•	align_x / align_y / right_of
	•	Host/Array 같은 반복 배치
	3.	Hierarchy/Structure
	•	Structure 단위 생성
	•	Sub-structure 지원

B. Solver 확장
	1.	Deterministic linear solver → multi-dependency 처리
	2.	Constraint 처리
	•	Hard / Soft constraints
	•	Future: min/max size, proximity, stacking rules

C. Compiler / Lowering
	1.	OpenSCAD 출력 강화
	•	semantic 주석 포함
	•	hierarchy 표시
	2.	미래: IFC / glTF / 3D BIM 로워링
	3.	LLM 루프 친화적: 에러/워닝 line info 포함

D. TDD / 테스트 확장
	1.	Dependency & hierarchy 테스트 추가
	2.	Semantic 기반 수정 테스트
	3.	Constraint violation 테스트
	4.	Multi-cube, multi-structure 시나리오

E. LLM 통합 루프
	1.	compile() → errors/warnings → LLM 수정 → 재compile
	2.	Self-refinement: Hard constraints 위반 시 재조정
	3.	미래: AI-driven design assistant 완성

⸻

🔹 장기 목표
	•	2D → 3D 확장
	•	BIM 요소 추가: Wall, Slab, Door, MEP
	•	Graph-based reasoning & solver integration
	•	LLM-friendly DSL: Ark = AI-Driven Solver-Aided Design Language
