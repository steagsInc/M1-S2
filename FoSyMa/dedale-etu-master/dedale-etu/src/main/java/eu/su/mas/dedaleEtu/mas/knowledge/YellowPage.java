package eu.su.mas.dedaleEtu.mas.knowledge;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;

import eu.su.mas.dedale.mas.AbstractDedaleAgent;

public class YellowPage {
	
	private static YellowPage instance;
	
	private List<AbstractDedaleAgent> agents;
	
	public YellowPage() {
		this.agents = new ArrayList<AbstractDedaleAgent>();
	}
	
	public void register(AbstractDedaleAgent agent) {
		this.agents.add(agent);
	}
	
	public List<AbstractDedaleAgent> getOtherAgents(AbstractDedaleAgent agent){
		List<AbstractDedaleAgent> copie = new ArrayList<AbstractDedaleAgent>();
		for(AbstractDedaleAgent a :this.agents) {
			if(a!=agent) {
				copie.add(a);
			}
		}
		return copie;
	}

	public static YellowPage getinstance() {
		if (instance==null) {
			instance=new YellowPage();
		}
		
		return instance;
	}
	
}
