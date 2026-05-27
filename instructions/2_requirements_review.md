
# Overview

The first formal review of the design process is called **requirement review (RR)**; it is closely followed by the **system design review (SDR)**. In our class, we will combine the two into a single document.  This will include two parts:

- Requirements for the problem definition/explication (RR)
- Allocation of problem requirements to technology capabilities (SDR)

As a group, you are expected to present a formal RR/SDR for the single project idea (i.e. the problem statement addressed by a core technology) that you have selected as a group.

# General description (Framework)

## References

- Video – Using the following links review the class design lectures:
    - D3: Requirements Definition
        - <https://drive.google.com/file/d/1HjtkVHUR3W1OAWq2NVc96RjsNudwudWB/view>
    - D4: Design Methods: Creative
        - <https://drive.google.com/file/d/1HjtkVHUR3W1OAWq2NVc96RjsNudwudWB/view>
    - D5: Design Methods: Rational 1
        - <https://drive.google.com/file/d/1Ovkt_7rHljucLcQOFC6g_UUV4yz0oetO/view>
    - A3: Design for debugging
        - <https://ucla.app.box.com/s/mvodqbsxgo8ei3zn4yg50p7g7orbmzps>
    - Youtube: Quality Function Deployment (QFD) and House of Quality
        - <https://youtu.be/u9bvzE5Qhjk>

- Class Notes – The associated class notes to the design videos are available using the following links
    - <http://bionics.seas.ucla.edu/education/MAE_162/MAE_162DE_04.pdf>
    - <http://bionics.seas.ucla.edu/education/MAE_162/MAE_162DE_05.pdf>

- Example dependency diagrams
    - <https://capstone.uclalemur.com/pdf/Censi-diagrams.pdf>
        - Courtesy Andrea Censi (ETH Zürich) <https://censi.science/>

- Book Chapter Reference 1 -  Read Chapters 6-7
    - Paul Johannesson Erik Perjons, An Introduction to Design Science
    - <https://link.springer.com/book/10.1007/978-3-319-10632-8>
    - Note – Free access is available through the UCLA library via VPN

- Book Chapter Reference 2 – Read Chapters 6-9: Nigel Cross, Engineering Design Methods (Provided as Appendix B)

## Writeup

Your writeup should contain the following information to accomplish the objectives of the RR / SDR.

- Problem explication (Can be adapted from earlier project deliverables)
- Requirements definition (Address each one of the topics)
    - Objective tree method
    - Performance specification method
    - Quality function deployment methods
- Block diagrams of the system
- Allocation of requirements to individual configuration items (i.e. subsystems, represented by blocks in the diagram)

### Detailed Description

**Note:** The following two analyses (Part 1 and Part 2) should be made on the one selected idea you have chosen to work on as the core of your project.

#### Part 1: Requirements Definition

- Element Definition - Identify the artifact context and anatomy and clearly describe them
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

- Analysis - Use all the following methods and perform the analysis on the problem (See Appendix A for the steps). Describe each step in each method and the end result of each method. Since you may not have an opportunity to interact with real customers, use the other group members as your customers.
    - Objective Tree Method
    - Performance Specification Method
    - Quality Function Deployment Methods

#### Part 2: System Design - Block Diagrams

- Define the subsystem breakdown of your overall system.  Each subsystem will likely be hierarchically composed of smaller subsystems as well.  Describe the intended behavior (i.e. procedural reasoning) for each subsystem (i.e. configuration item), as decomposed into smaller behaviors as necessary.  Note that this breakdown should be driven by functionality as opposed to implementation---it is likely that several alternative components will be capable of performing a block's identified behavior; a single component may later prove capable of performing several blocks' behaviors as well.  Nonetheless, break down the overall system objective by its constituent functionality.

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

# Appendix A

##  Objective Tree Method – Summary
**Aim:** The aim of the objectives tree method is to clarify design objectives and sub objectives and the relationships between them.

1. Prepare a list of design objectives. These are taken from the design brief, from questions to the client, and from the discussion in the design team.
2. Order the list into sets of higher-level and lower-level objectives. The expanded list of objectives and sub objectives is grouped roughly into hierarchical levels.
3. Draw a diagrammatic tree of objectives, showing hierarchical relationships and interconnections. The branches (or roots) in the tree represent relationships which suggest means of achieving objectives.

**End Result:** Objective Tree


## Performance Specification Method – Summary

**Aim:** Make an accurate specification of the performance required of a design solution.

1. Consider the different levels of generality of solution which might be applicable.  There might be a choice between
    - Product alternatives
    - Product types
    - Product features
2. Determine the level of generality at which to operate. This decision is usually made by the client.  The higher the level of generality, the more freedom the designer has.
3. Identify the required performance attributes. Attributes should be stated in terms that are independent of any particular solutions.
4. State succinct and precise performance requirements for each attribute.  Wherever possible, specifications should be in quantified terms and identify ranges between limits.

**End Result:** Specification List (quantitative values or ranges)

## Quality Function Deployment Method– Summary

**Aim:** Set targets to be achieved for the engineering characteristics of a product, such that they satisfy customer requirements.

The procedure is as follows:

1. Identify customer requirements in terms of product attributes. It is important that 'the voice of the customer' is recognized, and those customer requirements are not subject to 'reinterpretation‘ by the design team.
1. Determine the relative importance of the attributes. Techniques of rank-ordering or points-allocation can be used to help determine the relative weights that should be attached to the various attributes. Percentage weights are normally used.
1. Evaluate the attributes of competing products. Performance scores for competing products and the design team's own product (if a version of it already exists) should be listed against the set of customer requirements.
1. Draw a matrix of product attributes against engineering characteristics. Include all the engineering characteristics that influence any of the product attributes and ensure that they are expressed in measurable units.
1. Identify the relationships between engineering characteristics and product attributes. The strength of the relationships can be indicated either by symbols or numbers; using numbers has some advantages, but can introduce a spurious accuracy.
1. Identify any relevant interactions between engineering characteristics. The 'roof' matrix of the 'house of quality' provides this check, but may be dependent upon changes in the design concept.
1. Set target figures to be achieved for the engineering characteristics. Use information from competitor products or from trials with customers.

**End Result:** House of Quality and Roof Diagram

## Brain Storming Protocol
- Duration: 20-30 min
- Group Leader Role
    - Formulate the problem statement used as a starting point  - Risks:
        - Too narrow – Limited range of ideas
        - Too vague – vague idea
    - The problem can often be usefully formulated as a question, such as "How can we improve on X?"
    - Ensure that the format of the method is followed
    - Ensure that it does not degenerate into a round-table discussion
- Step 1:
    - Spend a few minutes, in silence, writing down the first ideas that come into your head
- Step 2:
    - Each group member, in turn, read out one idea from his or her set.
    - The most important rule here is that negative feedback (e.g. "That's silly" or "That will never work") is not allowed from any other member of the group
- Step 3:
    - In response to every other person's idea is to try to build on it, to take it a stage further, to use it as a stimulus for other ideas, or to combine it with his or her own ideas.
    - Make a short pause after each idea is read out, to allow a moment for reflection and for writing down further new ideas.
- Step 4:
    - Classify the ideas into related groups

## Synectics Method Protocol
- **Starts with the 'problem as given'** -  the problem statement as presented by the client or company management.
- **Seek Analogies (Understand the Problem)** - help to 'make the strange familiar', i.e. expressing the problem in terms of some more familiar (but perhaps rather distant) analogy.
- **Conceptualization of the 'problem as understood'** – Understand the key factor or elements of the problem that need to be resolved, or perhaps a complete reformulation of the problem.
- **Seek Unusual & Creative Analogies (Create Solutions)** -  May lead to novel solution concepts. The analogies are used to open up lines of development which are pursued as hard and as imaginatively as possible by the group.


