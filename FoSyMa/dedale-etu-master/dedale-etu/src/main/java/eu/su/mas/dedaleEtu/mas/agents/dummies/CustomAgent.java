package eu.su.mas.dedaleEtu.mas.agents.dummies;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedale.mas.agent.behaviours.startMyBehaviours;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.AskStop;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.ReceiveMessageBehaviour;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.SendMap;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.Startingconversation;
import eu.su.mas.dedaleEtu.mas.behaviours.exploration.CustomExplorationBehaviour;
import eu.su.mas.dedaleEtu.mas.behaviours.exploration.ExploSoloBehaviour;
import eu.su.mas.dedaleEtu.mas.behaviours.knowledge.MappingBehaviour;
import eu.su.mas.dedaleEtu.mas.knowledge.MapRepresentation;
import eu.su.mas.dedaleEtu.mas.knowledge.YellowPage;
import jade.core.behaviours.Behaviour;

/**
 * <pre>
 * ExploreSolo agent. 
 * It explore the map using a DFS algorithm.
 * It stops when all nodes have been visited.
 *  </pre>
 *  
 * @author hc
 *
 */

public abstract class CustomAgent extends AbstractDedaleAgent {

	private static final long serialVersionUID = -6431752665590433727L;
	protected MappingBehaviour mapping;
	public MappingBehaviour getMapping() {
		return mapping;
	}

	protected CustomExplorationBehaviour explo;
	protected YellowPage yellowpage;
	protected List<Behaviour> lb=new ArrayList<Behaviour>();
	
	protected HashMap<String, Integer> conversations = new HashMap<String, Integer>();
	
	protected final int COOLDOWN =-5;
	
	protected void setup(){

		super.setup();
		
		this.mapping = new MappingBehaviour(this);
		this.yellowpage = YellowPage.getinstance();
		this.yellowpage.register(this);
		lb.add(this.mapping);
		lb.add(new AskStop(this));
		lb.add(new SendMap(this));
		lb.add(new Startingconversation(this));
		lb.add(new ReceiveMessageBehaviour(this));
		
		
		System.out.println("custom");

	}


	public CustomExplorationBehaviour getExplo() {
		return explo;
	}

	public YellowPage getYellowpage() {
		return yellowpage;
	}


	public int getConversationID(String agent) {
		if(!this.conversations.containsKey(agent)) this.conversations.put(agent, 0);
		if (this.conversations.get(agent)<0) this.conversations.put(agent, this.conversations.get(agent)+1);
		return this.conversations.get(agent);
	}
	
	public int newConversation(String agent) {
		this.conversations.put(agent,(int) (Math.random() * (99999)));
		
		return this.conversations.get(agent);
	}
	
	public int endConversation(String agent) {
		this.conversations.put(agent,COOLDOWN);
		
		return this.conversations.get(agent);
	}
	
	public List<String> getActiveConversations() {
		
		List<String> activeConversations = new ArrayList<String>();
		
		for(String a:this.conversations.keySet()) {
			if (this.conversations.get(a)>0) activeConversations.add(a);
		}
		
		return activeConversations;
	}

}
