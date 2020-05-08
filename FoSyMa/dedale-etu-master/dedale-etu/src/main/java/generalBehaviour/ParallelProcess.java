package generalBehaviour;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import dataStructures.tuple.Couple;
import dedale.agents.CustomAgent;
import dedale.agents.ExploreSoloAgent;
import dedale.behaviours.communication.ConversationCalling;
import dedale.behaviours.communication.ExchangeMap;
import dedale.behaviours.communication.position.BroadcastPosition;
import dedale.knowledge.MapRepresentation;
import dedale.knowledge.MapRepresentation.MapAttribute;
import eu.su.mas.dedale.env.Observation;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import jade.core.behaviours.Behaviour;
import jade.core.behaviours.FSMBehaviour;
import jade.core.behaviours.ParallelBehaviour;
import jade.core.behaviours.SimpleBehaviour;


import java.util.LinkedList;

public class ParallelProcess extends ParallelBehaviour {
    CustomAgent myAgent;
    LinkedList<Behaviour> protocoles = new LinkedList<>();

    public ParallelProcess(CustomAgent myAgent, Behaviour ... other_behaviours){
        super(myAgent,WHEN_ANY);
        this.myAgent = myAgent;
        for (Behaviour b:other_behaviours)
        {
            addSubBehaviour(b);
            this.protocoles.add(b);
        }
    }

    @Override
    public int onEnd() {
        int cpt = 0;
        for (Behaviour o:protocoles)
        {
            cpt = cpt + o.onEnd();
        }
        return cpt;
    }

}