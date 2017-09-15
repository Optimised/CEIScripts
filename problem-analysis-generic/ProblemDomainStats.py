#!/usr/bin/python

import ExtractSuccess
import ExtractRunningTime
import ExtractStatesEval
import ExtractDeadEnds

class ProblemDomainStats:

	SUCCESS_IDX = 0
	COMP_TIME_IDX = 1
	H_TIME_IDX = 2
	STATES_EVAL_IDX = 3
	H_STATES_EVAL_IDX = 4
	DEAD_ENDS_IDX = 5

	def __init__(self, plannerName, problemDomain):
		self.plannerName = plannerName
		self.problemDomain = problemDomain
		self.stats = {}
		self.totalProbs = 0
		self.totalSuccess = 0.0
		self.avgCompTime = 0.0
		self.avgHTime = 0.0
		self.avgStates = 0.0
		self.avgHStates = 0.0
		self.avgDeadEnds = 0.0

	def getProblemSuccess(self, problem):
		return self.stats[problem][self.SUCCESS_IDX]

	def getProblemCompTime(self, problem):
		return self.stats[problem][self.COMP_TIME_IDX]

	def getProblemHTime(self, problem):
		return self.stats[problem][self.H_TIME_IDX]

	def getProblemStatesEval(self, problem):
		return self.stats[problem][self.STATES_EVAL_IDX]

	def getProblemHStatesEval(self, problem):
		return self.stats[problem][self.H_STATES_EVAL_IDX]

	def getProblemDeadEnds(self, problem):
		return self.stats[problem][self.DEAD_ENDS_IDX]

	def createDataStructure(self, problemName):
		if problemName not in self.stats:
			self.stats[problemName] = {}
			self.stats[problemName][self.SUCCESS_IDX] = {}
			self.stats[problemName][self.COMP_TIME_IDX] = {}
			self.stats[problemName][self.H_TIME_IDX] = {}
			self.stats[problemName][self.STATES_EVAL_IDX] = {}
			self.stats[problemName][self.H_STATES_EVAL_IDX] = {}
			self.stats[problemName][self.DEAD_ENDS_IDX] = {}

	def processProblemLog(self, problemName, probNumber, logBuffer):
		self.totalProbs += 1

		self.createDataStructure(problemName)

		#Problem Success
		success = ExtractSuccess.extractSuccess(logBuffer)
		if self.plannerName == "lpg-td":
			success = ExtractSuccess.extractLPGTDSuccess(logBuffer)
		
		self.stats[problemName][self.SUCCESS_IDX][probNumber] = success
		self.totalSuccess += success
		
		#Computational Time
		compTime = ExtractRunningTime.extractRunTime(logBuffer)
		self.stats[problemName][self.COMP_TIME_IDX][probNumber] = compTime
		if compTime is not None:
			self.avgCompTime += compTime
		
		#Heuristic Time
		hTime = ExtractRunningTime.extractHRunTime(logBuffer)
		self.stats[problemName][self.H_TIME_IDX][probNumber] = hTime
		if hTime is not None:
			self.avgHTime += hTime
		
		#States Evaluated
		statesEval, hStates, totalStates = ExtractStatesEval.extractStatesEvaluated(logBuffer)
		self.stats[problemName][self.STATES_EVAL_IDX][probNumber] = statesEval
		self.stats[problemName][self.H_STATES_EVAL_IDX][probNumber] = hStates
		if statesEval is not None:
			self.avgStates += statesEval
		if hStates is not None:
			self.avgHStates += hStates
		
		#Deadends Encountered
		deadEnds = ExtractDeadEnds.extractDeadEndsManually(logBuffer)
		self.stats[problemName][self.DEAD_ENDS_IDX][probNumber] = deadEnds
		if deadEnds is not None:
			self.avgDeadEnds += deadEnds