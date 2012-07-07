/*
 *  DefiniensRuleset.h
 *  DefiniensRulesetColours
 *
 *  Created by Pete Bunting on 22/02/2008.
 *  Copyright 2008 Aberystwyth University. All rights reserved.
 *
 */

#ifndef DefiniensRuleset_H
#define DefiniensRuleset_H

#include <iostream>
#include <exception>
#include "DefiniensException.h"
//#include "DefiniensErrorHandler.h"
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/sax/HandlerBase.hpp>
#include <xercesc/util/XMLString.hpp>
#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/framework/LocalFileFormatTarget.hpp>
#include <iostream>
#include <fstream>
#include <string>

using namespace xercesc;

struct classColour
{
	const XMLCh *name;
	const XMLCh *red;
	const XMLCh *green;
	const XMLCh *blue;
};


class DefiniensRuleset
{
public:
	DefiniensRuleset(const char *ruleset) throw(DefiniensException);
	void standardiseColours(const char *parameters, const char *outputFile, bool blackBackground) throw(DefiniensException);
	void parseColourParamsFile(const char *parameters, classColour *classColours) throw(DefiniensException);
	void convertLineToClassColour(classColour *tmpClassColour, std::string *strLine);
	int countColourParamsFile(const char *parameters) throw(DefiniensException);
	~DefiniensRuleset();
protected:
	void updateColour(DOMElement *classElement, const XMLCh *red, const XMLCh *green, const XMLCh *blue) throw(DefiniensException);
	int findColour(classColour *classColours, int numClassColours, const XMLCh *className);
	void printColours(classColour *classColours, int numClassColours);
	void checkName(classColour *classColours, int numClassColours, const XMLCh *className, DOMElement *classElement);
	DOMBuilder *parser;
	DOMDocument *doc;
};
#endif

// EOF
