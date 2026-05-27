

# General Description

## Scope

As a group, you are expected to present a Preliminary Design Review (PDR).  The PDR demonstrates that the preliminary design meets all system requirements with acceptable risk within the cost and schedule constraints, and establishes the basis for proceeding with detailed design. It will show that the correct design options have been selected, interfaces have been identified, and verification/validation methods have been planned and described.

## Objectives

The following are typical objectives of a PDR:

- **Problem**– Ensure that the problem is clearly defined and well bounded.
- **Requirements**– Ensure that all system requirements have been identified, verified, and allocated.
- **Function/Performance**– Show that the proposed design is expected to meet the functional and performance system requirements.
- **Maturity**– Show sufficient detail and completeness in the proposed design approach to support proceeding along the process towards the critical and final design reviews (CDR and FDR).
- **Risks**– Show that the design is verifiable and that the risks have been identified, characterized, and mitigated where appropriate. Risk mitigation may in part include "Plan B" alternatives at different levels of the system---from alternative individual subsystems all the way to a completely alternative design candidate.

# Forms and Due Dates

The PDR will be submitted using the following three deliverables, all due \due:

## Written Report

- **Content**– The written report will include all the information, analysis, and planning (timeline) of the rest of the design process along with the selection process for the final design candidate. The length of the written document is not specified but it should address all the items listed in this outline. 

- **Form**– Written report, unlimited number of pages.

- **Due date**– \due uploaded to Canvas.

## Oral Presentation

- **Content**– The oral presentation will include the highlights of the written report selected to most effectively communicate the objectives listed above. It should particularly focus on issues that you seek further inputs from the instructors / TAs / peers.

- **Form**– Your team will have 30 minutes to present your slides, with an additional 5 minutes thereafter for questions.  All team members are expected to speak/present.

- **Due date**– Slides \due uploaded to Canvas.

- **Note**– Review <https://uclalemur.com/home/presentation-tips> for how to make an effective presentation.

## Project plan/schedule

- **Content**– Your project plan should lay out in detail your expected efforts for the duration of the design process leading to your final design, capturing a comprehensive list of subsystems and engineering tasks including dependencies and hierarchies, personnel assignments, and schedule bounds.

- **Form**– Your team's Gitlab issue tracker should be fully populated with epics, milestones, and issues.

- **Due date**– \due via the Gitlab issue tracker.

# Report Content

**Note:** Some sections of the PDR were previously addressed throughout the quarter. These sections are listed again for completion, and can be copied into the PDR if they haven't changed. 

## Part 1: Explicate the Problem 

Review your write-up as suggested below. At the end of this part address the following questions specifically.  The scope of this section is to justify and support your answers.

### Fundamental Questions

- What is the overall problem that this project is trying to solve?
- Why should people (everyone) care about this problem and it's solution?
- What has been done so far to address this problem, and what is yet missing that needs your solution?
- What subset of the overall problem are you addressing in particular?
    - How will we know when this subproblem has been satisfactorily solved, using quantitative metrics?
	- How does addressing your subproblem meaningfully lead towards solving the big picture problem?
	- What is your specific approach to addressing your subproblem?
	- How can others be reasonably sure that this approach will result success within your team's constraints?

### General Notes

- Only a single problem should be included in this section.
- Based on what you have learned from previous presentations, experiences, feedback, etc., refine any earlier formulations of the problem. 

### Problem explication

- **Formulate the Problem Precisely**– Describe the problem in a precise but also concise, easily understandable manner.
- **Position and Justify the Problem**–
    - Context: Clarify in which practice the problem appears. Explain why the problem is important and to whom.
    - Ensure the problem is of general interest: Make clear that the problem is of interest not only to a local practice.
    - Ensure the problem is solvable: Analyze and scope the problem so that it becomes small enough to be solved within your team's personnel, time, and budget constraints.
- **Find the Root Cause**– Perform a root cause analysis using the fish bone diagram using the 5Ms
- **Define resources**–
    - **Specify the Sources of the Problem**– Describe the literature and the stakeholders that have previously identified, studied, and experienced the problem.
    - **Background / Related Work / References**– Address the following questions via content from cited references:
        -   What foundation and fundamentals need to be known in order to understand your problem, approach, and solution?
        -   What work has been done before on this specific problem?
        -   How do we know that your problem hasn't yet been satisfactorily solved?
        -   What are related problems that have been addressed, and what work has been done on those?
        -   What are unrelated problems that have employed specific aspects of your proposed approach or solution?
        -   How does this collection of past work contribute to your planned work?
- **Define Strategy & Methods**–
    - **Describe How the Problem Has Been Explicated**– Explain what has been done to explicate the problem---in particular, how the stakeholders have been involved and how the research literature has been reviewed.
    - **Research Methods**– Identify the chosen research methods that you have used for the purpose of defining the problem, end describe the outcomes of your execution. You may have used additional methods (such as interviewing experts in the field) in addition to:
        - **Similar products**– Look for similar products in the market and compare them to your proposed product.
        - **Scientific papers**– Search for scientific papers related to the problem/application and your proposed product or its subsystems.  Cite the references at the end of your report and add soft copies of these papers in the appendix.
        - **Market assessment**– Study the market via statistical information or a dialogue with stakeholders. Who are your customers? What is the market cap (total number of customers)? 

- **Fundamental Questions**– Address the fundamental questions listed at the beginning of this part 

## Part 2: Requirements definition

- **Element Definition**– Identify the artifact context and anatomy and clearly describe them
    - Intended practice / other practice
    - Artifact
    - Problem
    - Technology
    - Uses
    - Perception
    - Addresses
    - Environment
    - Function
    - Behavior
    - Structure
    - Intended effects
    - Side effects

- **Analysis**– Use all the following methods and perform the analysis on the problem. Describe each step in each method and the end result of each method. Since you may not have an opportunity to interact with real customers, use the other group members as your customers.
    - Objective Tree Method
    - Performance Specification Method
    - Quality Function Deployment Methods

## Part 3: Development of design candidates

- **Creative Methods**: Use at least one of the following creative methods and documents the end result of the analysis using them:
	- **Brainstorming**– Conduct a brainstorm session led by the group leader and documents the different ideas presented by the group members. 
	- **Synectics**– Conduct a Synectics session and use one or more of the analogy methods to define potential solution (Direct Analogy, Personal Analogy, Symbolic Analogy, Fantasy Analogy). Note that you may use more than one analogy method.  Document the method that was used and the outcome.  
	- **Enlarged Search Space**– Enlarge the search space by using one or more of the following methods: Transformation, Random Input, Why-Why-Why, Counter Planning, Generalization.  Document the method that was used and the outcome.  
- **Rational Methods**: Use the following rational methods and documents the end result of the analysis using them
	- **Morphological Chart**– Based on the creative methods formulate the morphological chart including 
		- Sub Function – The first column of the chart 
		- Solutions – Three to five solutions to each function       

	    Extract from the morphological chart at least three comprehensive solutions including different combinations of the solutions to the individual sub functions
	- **Weighted Objectives**–
		-   Objective tree – Review and improve your objective tree by adding branches to the tree as needed.  
		-   Weighted objective chart – Create the chart using the following steps.
			1.  List the design objectives - These may need modification from an initial list.  An objectives tree can also be a useful feature of this method.
			2.  Rank-order the list of objectives - Pair-wise comparisons may help to establish the rank order.
			3.  Assign relative weightings to the objectives - These numerical values should be on an interval scale an alternative is to assign relative weights at different levels of an objectives tree, so that all weights sum to 1.0.
			4.  Tabulate the objectives parameters for each design candidate   
			5.  Establish performance parameters or utility scores for each of the objectives - Both quantitative and qualitative objectives should be reduced to performance on simple points scales.
			6.  Calculate and compare the relative utility values of the alternative designs - Multiply each parameter score by its weighted value: the 'best' alternative has the highest sum value. Comparison and discussion of utility value profiles may be a better design aid than simply choosing the 'best'. 
-   Rank the design candidates 

## Part 4: Design Candidate Selection

Given all the design methods that you have used, select the best design candidate that addresses the problem and the requirements.  Also include "Plan B" alternatives at different levels of the system---from alternative individual subsystems all the way to a completely alternative design candidate.  Justify this selection qualitatively and quantitatively. 

## Part 5: System Design - Block Diagram & System Component Specification

- Define the subsystem breakdown of your overall system.  Each subsystem will likely be hierarchically composed of smaller subsystems as well.  Describe the intended behavior (i.e. procedural reasoning) for each subsystem (i.e. configuration item), as decomposed into smaller behaviors as necessary.  Note that this breakdown should be driven by functionality as opposed to implementation---it is likely that several alternative components will be capable of performing a block's identified behavior; a single component may later prove capable of performing several blocks' behaviors as well.  Nonetheless, break down the overall system objective by its constituent functionality.

  Characterize, quantitatively specify, and select (or identify options for) the necessary components, which may include: 
	- **Sensors**– List all the properties you wish to measure and identify options for sensors that can sense the required property. Sensors may vary in accuracy, resolution, physical principles, the environment that they can operate in (air / water), and cost.
	- **Actuators**– Select the type(s) of actuation systems (e.g. motors---DC brushed/brushless, stepper, servo, AC---or solenoids, hydraulics, pneumatics, etc.) appropriate to your application as well as any necessary transmissions, weight or size bounds, or proprioceptive sensing based on the requirements i.e. loads, power (torque, force, speed), and operational environment.
	- **Algorithms**– Characterize the necessary computational behaviors of the design, and identify candidate algorithms.  Find existing libraries, packages, or other implementations to include in your codebase.
	- **Power supply**– Identify the power source based on the power requirements and identify how the source is to be replenished over the product lifetime.
	- **Mechanisms**– Identify all the mechanisms that are required to perform the mechanical functions of the system that you develop.
	- **Structures / Packaging**– Characterize the overall structure in terms of geometry, materials, strength, and aesthetics.
	- **CPU & Data Acquisition**– Identify the required number of analog I/O and digital I/O ports, along with the processor that will control the system and collect the data.
	- **Cables and Cable Management**– Identify all the cables (electrical / mechanical) along with type (round / flat), number of conductors, gauge, grounded / shielding, and cable management (fixing and manipulation in case of motion).
	- **Communication**– Identify all the modes of communication internally within the system and externally (i.e. transmitting data)
	- **Interface**– Define all the input/output elements indicating the status of the system (on/off, fault alerts) and visual/auditory/haptic information that should be communicated to the users, along with corresponding elements for getting information from users.
	- **Operational Modes**– Define all the operational modes of the system e.g. ideal, data collection, operation, data transmission etc.
- Wire the subsystem blocks into a procedural / functional block diagram
    - Clearly identify and define functional (i.e. data flow) inputs/outputs of each block
    - Characterize input/output specifications of each subsystem as best as you can, or identify how you plan to generate such specifications
    - Ensure that you have comprehensively captured the inputs/outputs for the system as a whole, as distributed to / gathered from the inputs/outputs of the subsystems

- Wire the same subsystem blocks into a dependency diagram
    - Clearly identify and define capabilities and costs / requirements of each block
    - Identify how the problem explication (requirements) map into this dependency diagram
    - If any capabilities or costs are unmatched within the scope of your project, identify how they will be addressed externally, e.g.:
        - Unconstrained capabilities could perhaps be specified through user studies, market research, simulation or prototype experiments, kept as a design parameter to be addressed generally, etc.
        - Unhandled costs may be addressed by outsourced / externally validated technical solutions, kept as a design parameter to be addressed generally, left as future work, etc.
        - Justify that your scope of project will still provide value despite such unmatched dependencies
    - Identify critical challenges / risks in realizing the desired system, i.e. highlight the wires (representing costs supported by capabilities) that will either be:
        - most difficut to meet, or
        - most impactful on final system value.

## Part 6: User interaction / experience

For the selected design candidate (and optionally a backup), provide the basic design of the interactions between the human elements and the rest of your system.

## Part 7: Conceptual Design (Sketches) & Aesthetics

Generate preliminary sketches of the system as a whole, along with its internal mechanism that will guarantee its functional operation. The system should be protected from its operational environment and vice versa with specific attention to both form and function (i.e. aesthetics and behavior).

## Part 8: Broader Impact

All products have direct effects, both positive (solving the problem) and negative (incurring a cost), these should be explored and characterized in the above sections.  They also have side effects that form the focus of this part of the report, i.e. consequences not directly related to the core problem.  For example, automation generally disrupts existing jobs; manufacturing has environmental impacts; nearly every new solution/practice will disrupt an old solution/practice; outcomes may be only accessible to a subset of the population causing an impact on the remainder.

For your chosen project, identify several noteworthy negative externalities (broader consequences to the world) associated with the adoption of your designed product.  Then, apply at least one ethical framework (e.g. deontology, consequentialism, etc) to justify why your project is ethically responsible to implement despite those externalities.

## Part 9: Tasks & Gantt Chart

Using the Gitlab issue tracker, generate a project plan from the completion of this PDR and continuing to the end of the academic year.  You may include tasks in spring break week, but that is not expected.  Export the resulting auto-generated Gantt chart and include it legibly in your PDR document.  Be sure to look over the generated Gantt chart itself for accuracy and completeness---if the chart looks wonky, it is likely that your Gitlab issues have been incompletely or incorrectly filed.

Include in your project plan the following characteristics:

- **Subsystems**– The project should be divided into (largely independent) subsystems, represented by epics in Gitlab.  Explain the functionality of each subsystem and its preconditions (assumptions) and postconditions (guarantees) in the epic description.
- **Milestones**– Set a milestone characterizing expected (system) capabilities and associated demonstration deliverables for each week of the project.  There should be additional deliverables associated with the following specific milestones:
    - Preliminary demo / storyboard during finals week of Winter quarter
    - Critical design review at week 5 of Spring quarter
    - Final design review at week 10 of Spring quarter
    - Final demo during finals week of Spring quarter
- **Tasks & Subtasks**– The development of each subsystem should be divided into tasks and subtasks, represented by individual issues filed in your Gitlab issue tracker.  Subtasks are represented in Gitlab by linked checkboxes in the task descriptions along with the respective issue relationships.  Be sure to also include internal and external communication tasks, and include time during the project for preparing reports and presentations. 
- **Task Dependencies**–  Define task dependencies between the subtasks indicating tasks that cannot begin before the previous task was completed, with blocking dependencies represented in Gitlab with the appropriate issue relationships.
- **Human Resources Assignments**– Assign a single group member to each task; they will be the one leading that effort, and will be responsible for ensuring the successful completion of that issue.  A task may require multiple members of the team to work together; nonetheless, only one team member should be assigned to oversee that effort and will be held accountable for its success.
- **Timeframes**– Allocate a timeframe (both a due date / deadline and a start date / expected duration) for each task. Timeframes will likely overlap since different group members will be working on different aspects of the problem at the same time.  Expect that every group member has at least one task allocated at any given time.

## Part 10: Draft Budget

Prepare a draft of a budget for the design process divided into the following two parts.  Note that this is for the design process, not the product---it should reflect the budget for prototyping over the duration of this course, not the cost associated with production to market after your final design review (FDR).

- **Supplies & Equipment**– Include the list of the parts that must be purchased, their quantity, and expected cost, ideally with the vendors and part numbers.  
- **Labor & Human Resources**– Include labor in your budget in terms of engineer-hours associated with the different core components of the design process leading to the FDR.  This will likely be extracted from and should align with your project plan / Gantt chart.

##   Part 11: Deliverables

In order to justify your final product design at your FDR, your engineering efforts will result in a variety of support / validation for the design decisions you make along the way.  Describe the content you will generate over the course of your project plan.  Robotic projects naturally vary in scope and focus, but the expected deliverables will likely be subsets of the following: 

- **Hardware Design**– Mechanical design of the hardware including CAD drawings and assemblies of all the parts as well as individual parts, including dimensions and tolerances
- **Computation**– Validated implementation of algorithms in code, along with operational analysis and certification via both subsystem test harnesses and end-to-end scenarios 
- **Simulations**– Specify the type of analyses that you plan to conduct to complete the project.  Include statistical characterization across noise/uncertainty, environments, usage, and other forms of variability.  Example simulations typically include:
    -   Finite element modeling for forces, deformations, and robustness of structures
    -   Dynamics & control analysis for stability and performance of feedback loops
    -   Functional analysis for quantification of behavioral accuracy
    -   User interactions and experience (UI/UX)

    Other examples of helpful simulations may include:

    -   Heat transfer / fluid flow analysis
    -   Peak / transient / steady state power modeling
    -   Tolerance stacking
    -   Autonomy
    -   Failure analysis

- **Integrated prototype**– Specify the subsystem(s) of your entire project that you plan to build as a proof of concept. This should capture the most critical (i.e. risky) part of the system as a whole such that successful demonstration of its functionality will guarantee the success of the subsequent product as a whole.
- **Contributions**– Given this framework, specify the expected contributions of your project, i.e. the value your team is expected to generate for future design teams that will take a future product to market to address the overarching problem.
