#include <iostream>
#include "DefiniensRuleset.h"

class Control
	{
	public:
		void runDefiniensRulesetColours(const char *ruleset, const char *parameters, const char *outputFile, bool blackBackground);
	};


void Control::runDefiniensRulesetColours(const char *ruleset, const char *parameters, const char *outputFile, bool blackBackground)
{
	try
	{
		DefiniensRuleset *defRuleset = new DefiniensRuleset(ruleset);
		defRuleset->standardiseColours(parameters, outputFile, blackBackground);
	}
	catch(DefiniensException e)
	{
		std::cout << "DefiniensException thrown: " << e.what() << std::endl;
	}
	
}

int main (int argc, char * const argv[]) 
{
	std::cout << "Number Arguments: " << argc-1 << std::endl;
	if(argc != 5)
	{
	    std::cout << "Requires 4 inputs\n";
	    std::cout << "./definienscolours <input_process_tree> <parameters_file> <output_process_tree> <leave_unknown_colours (0|1) 1=leave>\n";
	    std::exit(1);
	}
	const char *ruleset = "";
	const char *parameters = "";
	const char *outputFile = "";
	bool blackBackground = false;
	
	for(int i = 0; i < argc; i++)
	{
	    std::cout << i << ": '" << argv[i] << "'" << std::endl;
	    if(i == 1)
	    {
	   		ruleset = argv[i];
	    }
		else if(i == 2)
	    {
			parameters = argv[i];
	    }
	    else if(i == 3)
	    {
			outputFile = argv[i];
	    }
	    else if(i == 4)
	    {
			if(atoi(argv[i])==0)
			{
				blackBackground = true;
			}
			else if(atoi(argv[i])==1)
			{
				blackBackground = false;
			}
			else
			{
				std::cout << "Leave unknown classes has to be 1 or 0\n";
				std::cout << "./definienscolours <input_process_tree> <parameters_file> <output_process_tree> <leave_unknown_colours (0|1) 1=leave>\n";
	    		std::exit(1);
			}
	    }
	}

    Control *ctrl = new Control();
	ctrl->runDefiniensRulesetColours(ruleset, parameters, outputFile, blackBackground);
	delete ctrl;
    return 0;
}

// EOF
