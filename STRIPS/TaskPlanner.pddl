(define (domain nosliw)
    (:requirements :strips :typing)
    (:types 
        item agent location - object
        item agent - item_agent
        sword pen diamond spellbook amulet talisman - item
        hero dragon wizard - agent
        sorceress - wizard
        town mountain cave - location)
          
    (:predicates 
        (at ?x - item_agent ?y - location)
        (asleep ?x - dragon)
        (dead ?x - dragon)
        (safe ?x - town)
        (hasMagicalStrength ?x - hero)
        (different ?x ?y - item)
        (possesses ?x - agent ?y - item)
        (path-from-to ?x ?y - location))
      

    (:action travel
        :parameters
            (?a - hero ?from ?to - location)
        :precondition
            (and
                (at ?a ?from)
                (path-from-to ?from ?to))
        :effect 
            (at ?a ?to))

    (:action trade
        :parameters
            (?a ?b - agent ?loc - location ?item1 ?item2 - item)
        :precondition
            (and
                (at ?a ?loc)
                (at ?b ?loc)
                (possesses ?a ?item1)
                (possesses ?b ?item2))
        :effect
            (and
                (possesses ?a ?item2)
                (possesses ?b ?item1)
                (not (possesses ?a ?item1))
                (not (possesses ?b ?item2))))
        
    (:action pickup
        :parameters
            (?a - hero ?loc - location ?item - item)
        :precondition
            (and
                (at ?a ?loc)
                (at ?item ?loc))
        :effect
            (and
                (possesses ?a ?item)
                (not (at ?item ?loc))))
                
    (:action drop
        :parameters
            (?a - hero ?loc - location ?item - item)
        :precondition
            (and
                (at ?a ?loc)
                (possesses ?a ?item))
        :effect
            (and
                (not (possesses ?a ?item))
                (at ?item ?loc)))
                
    (:action magic
        :parameters
            (?a - hero ?b - wizard ?loc - location ?d1 ?d2 ?d3 - diamond)
        :precondition
            (and
                (at ?a ?loc)
                (at ?b ?loc)
                (possesses ?a ?d1)
                (possesses ?a ?d2)
                (possesses ?a ?d3)
                (different ?d1 ?d2)
                (different ?d1 ?d3)
                (different ?d2 ?d3))
        :effect
            (and
                (possesses ?b ?d1)
                (possesses ?b ?d2)
                (possesses ?b ?d3)
                (hasMagicalStrength ?a)
                (not (possesses ?a ?d1))
                (not (possesses ?a ?d2))
                (not (possesses ?a ?d3))))        
                
    (:action song
        :parameters
            (?a - hero)
        :precondition
            (possesses ?a quill)
        :effect
            (and
                (asleep nosliw)
                (safe happydale)))
            
    (:action slaying
        :parameters
            (?a - hero ?loc - location)
        :precondition
            (and
                (at ?a ?loc)
                (hasMagicalStrength ?a)
                (not (dead nosliw))
                (at nosliw ?loc))
        :effect
            (and
                (dead nosliw)
                (safe happydale)))
)



























































