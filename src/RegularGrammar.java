import java.util.List;
import java.util.Map;

public class RegularGrammar {
    char startSymbol;
    List<Character> terminals;
    List<Character> variables;
    Map<String, List<String>> productionRules;

    public RegularGrammar() {

    }

    public char getStartSymbol() {
        return startSymbol;
    }

    public void setStartSymbol(char startSymbol) {
        this.startSymbol = startSymbol;
    }

    public List<Character> getTerminals() {
        return terminals;
    }

    public void setTerminals(List<Character> terminals) {
        this.terminals = terminals;
    }

    public List<Character> getVariables() {
        return variables;
    }

    public void setVariables(List<Character> variables) {
        this.variables = variables;
    }

    public Map<String, List<String>> getProductionRules() {
        return productionRules;
    }

    public void setProductionRules(Map<String, List<String>> productionRules) {
        this.productionRules = productionRules;
    }
}
