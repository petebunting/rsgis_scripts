/*
 *  DefiniensRuleset.cpp
 *  DefiniensRulesetColours
 *
 *  Created by Pete Bunting on 22/02/2008.
 *  Copyright 2008 Aberystwyth University. All rights reserved.
 *
 */

#include "DefiniensRuleset.h"

DefiniensRuleset::DefiniensRuleset(const char *ruleset) throw(DefiniensException)
{
	parser = NULL;
	doc = NULL;
	
	try 
	{
		XMLPlatformUtils::Initialize();
	}
	catch (const XMLException& toCatch) 
	{
		char *message = XMLString::transcode(toCatch.getMessage());
		std::cout << "Error during initialization! :\n" << message << "\n";
		XMLString::release(&message);
	}
	
	XMLCh tempStr[100];
	XMLString::transcode("LS", tempStr, 99);
	DOMImplementation *impl = DOMImplementationRegistry::getDOMImplementation(tempStr);
	if( impl == 0 )
	{
		throw DefiniensException("impl == 0: Could not create DOM implementation");
	}
	parser = ((DOMImplementationLS*)impl)->createDOMBuilder(DOMImplementationLS::MODE_SYNCHRONOUS, 0);
	try 
	{
		doc = parser->parseURI(ruleset);
	}
	catch (const XMLException& toCatch) {
		char* message = XMLString::transcode(toCatch.getMessage());
		std::cout << "Exception message is: \n" << message << "\n";
		XMLString::release(&message);
	}
	catch (const DOMException& toCatch) 
	{
		char* message = XMLString::transcode(toCatch.msg);
		std::cout << "Exception message is: \n" << message << "\n";
		XMLString::release(&message);
	}
}


void DefiniensRuleset::standardiseColours(const char *parameters, const char *outputFile, bool blackBackground) throw(DefiniensException)
{
	int numClassColours = this->countColourParamsFile(parameters);
	std::cout << "Parameters file has " << numClassColours << " lines of data\n";
	classColour *classColours = new classColour[numClassColours];
	this->parseColourParamsFile(parameters, classColours);
	this->printColours(classColours, numClassColours);
	
	DOMElement *rootElement = doc->getDocumentElement();
	std::cout << "Root Element: " << XMLString::transcode(rootElement->getTagName()) << std::endl;
	if(!XMLString::equals(rootElement->getTagName(), XMLString::transcode("eCog.Proc")))
	{
		throw DefiniensException("Incorrect root element");
	}
	
	DOMNodeList *classHrchy = rootElement->getElementsByTagName(XMLString::transcode("ClssHrchy"));
	int classHrchyNodesNum = classHrchy->getLength();
	std::cout << "classHrchy has " << classHrchyNodesNum << " nodes." << std::endl;
	
	if(classHrchyNodesNum != 1)
	{
		throw DefiniensException("Error: Multiple clsshrchy nodes defined.");
	}
	DOMElement *classHrchyRootElement = static_cast<DOMElement*>(classHrchy->item(0));
	
	DOMNodeList *allClasses = classHrchyRootElement->getElementsByTagName(XMLString::transcode("AllClss"));
	int numAllClasses = allClasses->getLength();
	std::cout << "allClasses has " << numAllClasses << " nodes." << std::endl;
	if(numAllClasses != 1)
	{
		throw DefiniensException("Error: Multiple allclss nodes defined.");
	}
	DOMElement *allClassesRootElement = static_cast<DOMElement*>(allClasses->item(0));
	
	DOMNodeList *classes = allClassesRootElement->getElementsByTagName(XMLString::transcode("Clss"));
	int numClasses = classes->getLength();
	std::cout << "classes has " << numClasses << " nodes." << std::endl;
	
	for(int i = 0; i < numClasses; i++)
	{
		DOMElement *classElement = static_cast<DOMElement*>(classes->item(i));
		const XMLCh *className = classElement->getAttribute(XMLString::transcode("name"));
		std::cout << "Found class with name " << XMLString::transcode(className) << std::endl;
		this->checkName(classColours, numClassColours, className, classElement);
		int index = this->findColour(classColours, numClassColours, className);
		if(index != -1)
		{
			this->updateColour(classElement, classColours[index].red, classColours[index].green, classColours[index].blue);
		}
		else if(blackBackground)
		{
			this->updateColour(classElement, XMLString::transcode("0"), XMLString::transcode("0"), XMLString::transcode("0"));
		}
	}
	
	try
	{
		XMLCh tempStr[100];
		XMLString::transcode("LS", tempStr, 99);
		DOMImplementation *impl = DOMImplementationRegistry::getDOMImplementation(tempStr);
		if( impl == 0 )
		{
			throw DefiniensException("impl == 0: Could not create DOM implementation");
		}
		
		DOMWriter* writer = ((DOMImplementationLS*)impl)->createDOMWriter();
		writer->setFeature(XMLUni::fgDOMWRTFormatPrettyPrint, false);
		LocalFileFormatTarget outputFileTarget(outputFile);
		writer->writeNode(&outputFileTarget, *rootElement);
		writer->release();
	}
	catch(const XMLException &e)
	{
		std::cout << "Error: XMLException: " << XMLString::transcode(e.getMessage()) << std::endl;
	}
	catch(const DOMException &e)
	{
		std::cout << "Error: DOMException: " << XMLString::transcode(e.getMessage()) << std::endl;
	}
	
}

int DefiniensRuleset::findColour(classColour *classColours, int numClassColours, const XMLCh *className)
{
	bool found = false;
	int index = -1;
	for(int i = 0; i < numClassColours; i++)
	{
		if(XMLString::equals(classColours[i].name, className))
		{
			std::cout << "Found class " << XMLString::transcode(className) << std::endl;
			index = i;
			found = true;
			break;
		}
	}
	if(!found)
	{
		std::cout << XMLString::transcode(className) << " has NOT been found in parameters file!\n";
	}
	return index;
}

void DefiniensRuleset::checkName(classColour *classColours, int numClassColours, const XMLCh *className, DOMElement *classElement)
{
	bool found = false;
	bool finished = false;
	bool newName = false;
	while(!finished & !found)
	{
		for(int i = 0; i < numClassColours; i++)
		{
			if(XMLString::equals(classColours[i].name, className))
			{
				found = true;
				finished = true;
			}
		}
		if(!found)
		{
			std::string text;
			std::cout << "Class \'" << XMLString::transcode(className) << "\' was not found please provide correct name (Press enter to ignore):\n";
			getline(std::cin, text);
			std::cout << "User input: " << text << std::endl;
			if(XMLString::equals(XMLString::transcode(text.c_str()), XMLString::transcode("")))
			{
				finished = true;
			}
			else
			{
				newName = true;
				className = XMLString::transcode(text.c_str());
			}
		}
		else if(newName & found)
		{
			std::cout << "Class has been renamed to " << XMLString::transcode(className) << std::endl;
			classElement->setAttribute(XMLString::transcode("name"), className);
		}
	}
	
}

void DefiniensRuleset::printColours(classColour *classColours, int numClassColours)
{
	for(int i = 0; i < numClassColours; i++)
	{
		std::cout << XMLString::transcode(classColours[i].name) << ": [" << XMLString::transcode(classColours[i].red) << "," << XMLString::transcode(classColours[i].green) << "," << XMLString::transcode(classColours[i].blue) << "]\n";
	}
}

void DefiniensRuleset::updateColour(DOMElement *classElement, const XMLCh *red, const XMLCh *green, const XMLCh *blue) throw(DefiniensException)
{
	static XMLCh *name = XMLString::transcode("Color");
	DOMNodeList *children = classElement->getChildNodes();
	int numChildren = children->getLength();
	for(int i= 0; i < numChildren; i++)
	{
		DOMNode *child = children->item(i);
		if(child->getNodeType() == DOMNode::ELEMENT_NODE)
		{
			DOMElement *childElement = static_cast<DOMElement*>(child);
			if(XMLString::equals(childElement->getTagName(), name))
			{
				//std::cout << "child node name: " << XMLString::transcode(static_cast<DOMElement*>(child)->getTagName()) << std::endl;
				//const XMLCh *currentRed = childElement->getAttribute(XMLString::transcode("R"));
				//const XMLCh *currentGreen = childElement->getAttribute(XMLString::transcode("R"));
				//const XMLCh *currentBlue = childElement->getAttribute(XMLString::transcode("B"));
				std::cout << "Colour: [" << XMLString::transcode(red) << "," << XMLString::transcode(green) << "," << XMLString::transcode(blue) << "]\n";
				childElement->setAttribute(XMLString::transcode("R"), red);
				childElement->setAttribute(XMLString::transcode("G"), green);
				childElement->setAttribute(XMLString::transcode("B"), blue);
			}
		}
	}
}

void DefiniensRuleset::parseColourParamsFile(const char *parameters, classColour *classColours) throw(DefiniensException)
{
	std::ifstream inFile;
	inFile.open(parameters);
	
	if(inFile.is_open())
	{
		int i = 0;
		std::string strLine;
		strLine.erase();
		
		while(!inFile.eof())
		{
			getline(inFile, strLine, '\n');
			if(strLine.size() != 0 && strLine.at(0) != '#')
			{
				classColour *tmpclassColours = new classColour();
				this->convertLineToClassColour(tmpclassColours, &strLine);
				//std::cout << "name: " << XMLString::transcode(tmpclassColours->name) << " R: " << XMLString::transcode(tmpclassColours->red) << " G: " << XMLString::transcode(tmpclassColours->green) << " B: " << XMLString::transcode(tmpclassColours->blue) << std::endl;
				classColours[i] = *tmpclassColours;
				i++;
			}
			strLine.erase();
		}
	}
	else
	{
		throw DefiniensException("Parameters file could not be openned");
	}
}

void DefiniensRuleset::convertLineToClassColour(classColour *tmpClassColour, std::string *strLine)
{
	//std::cout << "Line: " << strLine->c_str() << std::endl;
	
	tmpClassColour->name = XMLString::transcode("DEFAULT");
	tmpClassColour->red = XMLString::transcode("0");
	tmpClassColour->blue = XMLString::transcode("0");
	tmpClassColour->green = XMLString::transcode("0");
	
	int countTokens = 0;
	int lineLength = strLine->size();
	int start = 0;
	
	for(int i = 0; i < lineLength; i++)
	{
		if(strLine->at(i) == ';')
		{
			//std::cout << "Substring: " << strLine->substr(start, i-start) << std::endl;
			if(countTokens == 0)
			{
				//ignore
				countTokens++;
			}
			else if(countTokens == 1)
			{
				tmpClassColour->name = XMLString::transcode(strLine->substr(start, i-start).c_str());
				countTokens++;
			}
			else if(countTokens == 2)
			{
				tmpClassColour->red = XMLString::transcode(strLine->substr(start, i-start).c_str());
				countTokens++;
			}
			else if(countTokens == 3)
			{
				tmpClassColour->green = XMLString::transcode(strLine->substr(start, i-start).c_str());
				countTokens++;
			}
			else
			{
				std::cout << "There are too many columns in the text file.\n";
				std::exit(-1);
			}
			start = ++i;
		}
	}
	//std::cout << "Substring: " << strLine->substr(start) << std::endl; 
	tmpClassColour->blue = XMLString::transcode(strLine->substr(start).c_str());
}

int DefiniensRuleset::countColourParamsFile(const char *parameters) throw(DefiniensException)
{
	int i = 0;
	std::ifstream inFile;
	inFile.open(parameters);
	
	if(inFile.is_open())
	{
		std::cout << "File openned!\n";
		std::string strLine;
		strLine.erase();
		while(!inFile.eof())
		{
			getline(inFile, strLine, '\n');
			//std::cout << strLine.c_str() << std::endl;
			if(strLine.size() != 0 && strLine.at(0) != '#')
			{
				i++;
			}
			strLine.erase();
		}
	}
	else
	{
		throw DefiniensException("Parameters file could not be openned");
	}
	return i;
}

DefiniensRuleset::~DefiniensRuleset()
{
	parser->release();
}

// EOF
