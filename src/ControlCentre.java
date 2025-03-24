import java.util.List;

public class ControlCentre {
    List<RegularGrammar> regularGrammars;
    

    public void addRegularGrammar(RegularGrammar rg) {
        regularGrammars.add(rg);
    }

    public List<RegularGrammar> getRegularGrammars() {
        return regularGrammars;
    }

}
