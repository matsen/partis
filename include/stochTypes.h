#ifndef STOCHHMM_STOCHTYPES_H
#define STOCHHMM_STOCHTYPES_H
namespace stochhmm{
  //! \file stochTypes.h
  //! Stores enumerated types used in StochHMM library

  //Enumerated Transition identifiers
  //!\enum enum transType {STANDARD , USER , INTERNAL , LEXICAL};
  //!Types of Transitions
  //! STANDARD = Transition has log probability value
  //! USER = Transition is duration dependent and calculated by user defined distribution
  //! INTERNAL = Transition is duration dependent and calculated by internal defined distibution
  //! LEXICAL =  Transition is dependent upon the preceeding sequence
  enum transType {STANDARD , DURATION , LEXICAL, PDF};
    
    
  //!\enum tracebackIdentifier { DIFF_STATE , STATE_NAME , STATE_LABEL , STATE_GFF , START_INIT };
  //! Traceback identifier describe how stochHMM will traceback when using duration dependent distributions
  //! Types of Tracebacks
  //! DIFF_STATE = Traceback current state until a different state is encountered
  //! STATE_NAME = Traceback until STATE_NAME changes from current state, essentially the same as DIFF_STATE
  //! STATE_LABEL = Traceback until a State with a different label is encountered
  //! STATE_GFF = Traceback until a State witha a different GFF tag is encountered
  //! START_INIT = Traceback until the start of the sequence
  enum tracebackIdentifier { DIFF_STATE , STATE_NAME , STATE_LABEL , STATE_GFF , START_INIT };
    
    
  //!enum combineIdentifier { FULL , STATENAME , STATELABEL , STATEGFF};
  //!Describes how a traceback will be processed
  //! Types of Combine Identifiers
  //! FULL = No traceback editing will occur
  //! STATENAME = Edit out all the states that aren't of given State Name
  //! STATELABEL= Edit out all the states that aren't of given State Label
  //! STATEGFF  = Edit out all the states that aren't of given GFF Tag
  enum combineIdentifier { FULL , STATENAME , STATELABEL , STATEGFF};

  //Enumerated Trellis Types
  //!\enum trellisType {SIMPLE, STOCH, NTH};
  //!Defines what type of trellis cells to use
  //!Types of trellis
  //! SIMPLE = Trellis will only contain single viterbi, forward, and backward values
  //! STOCH  = Trellis will contain multiple viterbi,forward,backward values and traceback probabilities for stochastic tracebacks
  //! NTH = Trellis will contain N viterbi values for top N tracebacks 
  enum trellisType {SIMPLE, STOCH, NTH};
    
  //!\enum decodingType {VITERBI, POSTERIOR};
  //!Type of decoding to perform.
  //! VITERBI = Traceback performed using viterbi value
  //! FORWARD = Traceback performed using stochastic forward value
  //! POSTERIOR = Traceback performed using posterior value
  enum decodingType {VITERBI, FORWARD, POSTERIOR};

  //Enumerated Emission Track types
  //!Track types
  //! UNDEFINED = NOT DEFINED BY USER
  //! ALPHA_NUM = Alphabet is letter or word based (discrete)
  //! REAL = Real number values (continuous)
  //! EXTERNAL = ???
  enum trackType {UNDEFINED, ALPHA_NUM , REAL , EXTERNAL};


  //Enumerated Unknown Emission Character Probability Types
    
  //!enum unknownCharScoringType { DEFINED_SCORE, AVERAGE_SCORE, LOWEST_SCORE, HIGHEST_SCORE, NO_SCORE};
  //! How to score unknown or ambiguous characters when encountered in emission or transition
  //! Scoring types:
  //! DEFINED_SCORE = user-defined score
  //! AVERAGE_SCORE = average of all possible scores
  //! LOWEST_SCORE = lowest of the possible scores
  //! HIGHEST_SCORE = highest of the possible scores
  //! NO_SCORE = No score will be defined (Produces error if unknown alphabet encountered)
  enum unknownCharScoringType { DEFINED_SCORE, AVERAGE_SCORE, LOWEST_SCORE, HIGHEST_SCORE, NO_SCORE};
    
    
  //enum valueType {PROBABILITY, LOG_ODDS, COUNTS, LOG_PROB, PERCENTAGE};
  //!Value types that are provided by user
  //!PROBABILITY = basic probability between [0,1]
  //!LOG_ODDS = log odds score
  //!COUNTS = word counts
  //!LOG_PROG = log2 value of probability
  //!PERCENTAGE = [0,100] or 100*Probability
  enum valueType {UNKNOWN, PROBABILITY, LOG_ODDS, COUNTS, LOG_PROB, PERCENTAGE} ;


}
#endif
