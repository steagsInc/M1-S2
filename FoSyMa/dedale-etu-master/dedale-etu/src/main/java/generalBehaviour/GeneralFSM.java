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
import dedale.behaviours.communication.BroadcastWumpus;
import dedale.behaviours.communication.ConversationCalling;
import dedale.behaviours.communication.ExchangeMap;
import dedale.behaviours.communication.position.BroadcastPosition;
import dedale.behaviours.hunting.FollowWumpus;
import dedale.behaviours.hunting.GetAheadWumpus;
import dedale.behaviours.knowledge.WumpusScouting;
import dedale.knowledge.MapRepresentation;
import dedale.knowledge.MapRepresentation.MapAttribute;
import eu.su.mas.dedale.env.Observation;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import jade.core.behaviours.Behaviour;
import jade.core.behaviours.FSMBehaviour;
import jade.core.behaviours.ParallelBehaviour;
import jade.core.behaviours.SimpleBehaviour;


/**
 * This behaviour allows an agent to explore the environment and learn the associated topological map.
 * The algorithm is a pseudo - DFS computationally consuming because its not optimised at all.</br>
 * 
 * When all the nodes around him are visited, the agent randomly select an open node and go there to restart its dfs.</br> 
 * This (non optimal) behaviour is done until all nodes are explored. </br> 
 * 
 * Warning, this behaviour does not save the content of visited nodes, only the topology.</br> 
 * Warning, this behaviour is a solo exploration and does not take into account the presence of other agents (or well) and indefinitely tries to reach its target node
 * @author hc
 *
 */
public class GeneralFSM extends FSMBehaviour {
	
	private CustomAgent myAgent;
	
	

	public GeneralFSM(CustomAgent myagent) {
		super(myagent);
		this.myAgent = myagent;
		
		ParallelBehaviour exploProcess = new ParallelProcess(this.myAgent,"EXPLO",this.myAgent.getMapping(),new WumpusScouting(this.myAgent),new BroadcastWumpus(this.myAgent,BroadcastWumpus.role.Receiver),new ConversationCalling(this.myAgent),new BroadcastPosition(this.myAgent),this.myAgent.getExplo());
		
		ParallelBehaviour convoProcess = new ParallelProcess(this.myAgent,"CONVERSATION",new ExchangeMap(this.myAgent));
		
		ParallelBehaviour huntingProcess = new ParallelProcess(this.myAgent,"HUNTING",this.myAgent.getMapping(),new BroadcastPosition(this.myAgent),new FollowWumpus(this.myAgent,this.myAgent.getMapping()),new BroadcastWumpus(this.myAgent,BroadcastWumpus.role.Broadcaster));
		
		ParallelBehaviour scoutingProcess = new ParallelProcess(this.myAgent,"SCOUT",this.myAgent.getMapping(),new BroadcastPosition(this.myAgent),new WumpusScouting(this.myAgent),new BroadcastWumpus(this.myAgent,BroadcastWumpus.role.Receiver),new GetAheadWumpus(this.myAgent,this.myAgent.getMapping()));
		
		String [] explo = {"EXPLO"} ;
        String [] conversation = {"CONVERSATION"} ;
        String [] hunting = {"HUNTING"} ;
        String [] scout = {"SCOUT"} ;
        
        
        registerFirstState(exploProcess,"EXPLO");
        registerState(convoProcess,"CONVERSATION");
        registerState(huntingProcess,"HUNTING");
        registerState(scoutingProcess,"SCOUT");
        
        registerDefaultTransition("EXPLO","EXPLO",explo);
        registerTransition("EXPLO","EXPLO",0,explo);
        registerTransition("EXPLO","CONVERSATION",2,conversation);
        registerTransition("EXPLO","HUNTING",5,hunting);
        registerTransition("EXPLO","SCOUT",20,scout);
        registerTransition("EXPLO","SCOUT",21,scout);
        registerTransition("EXPLO","SCOUT",25,scout);
        
        registerDefaultTransition("CONVERSATION","EXPLO",explo);
        registerTransition("CONVERSATION","EXPLO",1,explo);
        
        registerDefaultTransition("HUNTING","HUNTING",hunting);
        registerTransition("HUNTING","HUNTING",0,hunting);
        registerTransition("HUNTING","EXPLO",10,explo);
        
        registerDefaultTransition("SCOUT","SCOUT",explo);
        registerTransition("SCOUT","SCOUT",0,hunting);
        registerTransition("SCOUT","HUNTING",5,hunting);
		
	}
	
}
