import java.io.IOException;

public class main {

	private int nl=1;
	private int nw=1;
	private int nc=1;
	/*private ;

	char c ;
	int indent;*/
    private String chaine="Wala permet la représentation du code dans une représentation intermédiaire, comprenant un CFG intra-procédural ainsi que les dernières instructions SSA de chaque bloc. Wala a également des interfaces permettant d'extraire d'autres graphes, tels que des CFG étendus ou des CFG inter-procéduraux. Il est ensuite possible de parcourir ces graphes afin de récolter des informations dans chaque noeud.\n" +
            "Pour l'analyse PTFA, nous avons besoin de connaitre les instructions affectant la sécurité, et donc de chaque instruction SSA. Pour cela, il parait plus pertinent d'utiliser un graphe étendu, c'est à dire avec un bloc pour chaque instruction. Ensuite, nous devrons considérer plusieurs contextes d'appels des méthodes lors de l'analyse. Nous devons donc extraire un graphe inter-procédural et étendu.";
    ;

    public static void main(String[] args)  {
        (new main()).wordcount();
    }
    public int wordcount(){
        nl=1;
        nw=1;
        nc=1;
        boolean inword= false;
        for(int indent=0; indent<chaine.length(); indent++){
        char c = chaine.charAt(indent);
        nc++;
        if (c=='\n') {
                nl++;
        }
        if(c=='\n'||c=='\t'||c==' '){
            if (!inword){
                inword=true;
                nw++;
            }
        }
        else{
            inword=false;
        }
        }

        return 0;
    }
}
