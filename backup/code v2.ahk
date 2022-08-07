#singleinstance force   ; prevents a message about closing running copy of script


;___________________________________________________________________________

f12:: ;<- toggle on and off

runtoggle := !runtoggle

if (!runtoggle)

{ SetTimer, runscript, off

  tooltip

  return

}

; drops through into the scrip timer and execution

runscript:

tooltip, dashboard script is running

FileDelete, info.txt
FileDelete, Agents.csv
FileDelete, Queue.csv

if WinExist("Amazon Connect - Real-time metrics - Google Chrome")
	{
   	WinActivate ; Use the window found by WinExist.
		SendInput ^a
		SendInput ^c
		x = %clipboard%
		FileAppend, %x% , info.txt	
	}


	
file := "info.txt"
AgtFile := "Agents.csv"
QueFile := "Queue.csv"

Varnum = 0
VarBool = False
StatNum = 0
NumAgents = 0
InSum = 0
OutSum = 0

Agents := []
Activity := []
Duration := []
AgentName := []
Handled_in := []
Handled_out := []
AHT := []


Queues := []
QueueOnline := []
QueueNPT := []
CallsInQueue := []
QueueOldest := []
QueueQueued := []
QueueHandled := []
QueueAbandoned := []
QueueAHT := []
QueueSLA := []


FileRead, LoadedText, %file%
; Split on new line
oText := StrSplit(LoadedText, "`n")
Loop, % oText.MaxIndex()
{
	S = % oText[A_Index]
	StringReplace,S,S,`n,,A
	StringReplace,S,S,`r,,A
	StringReplace,S,S,`t,,A
	S = %S%
	Switch Varnum
	{
	Case 0:
				;Msgbox, Test2 %VarBool%
				if (InStr(oText[A_Index], "Agent	Performance"))
					{
						VarBool = False
						Varnum += 1
					}

				if (%VarBool% == True)
					{
						;Msgbox, Test3
						if (!InStr(oText[A_Index], "Voice"))
						{
							Agents.Push(S)
							NumAgents += 1
						}
					}
	
				if (InStr(oText[A_Index], "Agent Login	Channels"))
					{
						VarBool = True
					}
					
	Case 1:
				if (InStr(oText[A_Index], "Rows per page: "))
					{
						VarBool = False
						Varnum += 1
						StatNum = 0
					}

				if (%VarBool% == True)
					{
						Switch StatNum
						{
						Case 1:
						{
							Activity.Push(S)
						}
						Case 2:
						{
							Duration.Push(S)
						}
						Case 3:
						{
							Comma := ","
							StringReplace,S,S,%Comma%,,A
							AgentName.Push(S)
						}
						Case 4:
						{
							Handled_in.Push(S)
						}
						Case 5:
						{
							Handled_out.Push(S)
						}
						Case 6:
						{
							AHT.Push(S)
						}
						Case 7:
						{
							Callback.Push(S)
						}
						}
						
						if (StatNum != 7)
							{
								StatNum += 1
							} else {
								StatNum = 1
							}
					}
	
				if (InStr(oText[A_Index], "Callback contacts handled"))
					{
						VarBool = True
						StatNum = 1
					}
					
		Case 2:
				if (InStr(oText[A_Index], "Agents	Performance"))
					{
						;Msgbox, Testing 1
						VarBool = False
						Varnum += 1
					}
				if (InStr(oText[A_Index], "Summary"))
					{
						;Msgbox, Testing 2
						VarBool = True
					}
				if (%VarBool% == True)
					{
						;Msgbox, Testing 3
						Queues.Push(S)
					}
		
		Case 3:
		{
				if (InStr(oText[A_Index], "Rows per page: "))
					{
						;Msgbox, Testing close
						VarBool = False
						Varnum += 1
						StatNum = 0
					}

				if (%VarBool% == True)
					{
						;Msgbox, % oText[A_Index] " testing add"
						Switch StatNum
						{
						Case 1:
						{
							QueueOnline.Push(S)
						}
						Case 2:
						{
							QueueNPT.Push(S)
						}
						Case 3:
						{
							CallsInQueue.Push(S)
						}
						Case 4:
						{
							QueueOldest.Push(S)
						}
						Case 5:
						{
							Comma := ","
							StringReplace,S,S,%Comma%,,A
							QueueQueued.Push(S)
						}
						Case 6:
						{
							Comma := ","
							StringReplace,S,S,%Comma%,,A
							QueueHandled.Push(S)
						}
						Case 7:
						{
							QueueAbandoned.Push(S)
						}
						Case 8:
						{
							QueueAHT.Push(S)
						}
						Case 9:
						{
							QueueSLA.Push(S)
						}
						}
						if (StatNum != 9)
							{
								StatNum += 1
							} else {
								StatNum = 1
							}
					}
	
				if (InStr(oText[A_Index], "SL 60 secs"))
					{
						VarBool = True
						StatNum = 1
					}
		}
		}
		
}


for k,v in Handled_in
	{
		InSum +=v
	}
	
for k,v in Handled_out
	{
		OutSum +=v
	}
	
FileAppend,
(
Agents, Activity, Duration, Agent Name, Handled in, Handled out, AHT

), Agents.csv

FileAppend,
(
Queue, Online, NPT, In queue, Oldest, Queued, Handled, Abandoned, AHT, SLA

), Queue.csv
	
	
for k, in Agents
	{
		FileAppend, % Agents[k] ", " , Agents.csv
		FileAppend, % Activity[k] ", " , Agents.csv
		FileAppend, % Duration[k] ", " , Agents.csv
		FileAppend, % AgentName[k] ", " , Agents.csv
		FileAppend, % Handled_in[k] ", " , Agents.csv
		FileAppend, % Handled_out[k] ", " , Agents.csv
		FileAppend, % AHT[k] "`n" , Agents.csv
	}
	
for k, in Queues
	{
		FileAppend, % Queues[k] ", " , Queue.csv
		FileAppend, % QueueOnline[k] ", " , Queue.csv
		FileAppend, % QueueNPT[k] ", " , Queue.csv
		FileAppend, % CallsInQueue[k] ", " , Queue.csv
		FileAppend, % QueueOldest[k] ", " , Queue.csv
		FileAppend, % QueueQueued[k] ", " , Queue.csv
		FileAppend, % QueueHandled[k] ", " , Queue.csv
		FileAppend, % QueueAbandoned[k] ", " , Queue.csv
		FileAppend, % QueueAHT[k] ", " , Queue.csv
		FileAppend, % QueueSLA[k] "`n" , Queue.csv
	}


FileCopy, Agents.csv, New_Agents.csv, Overwrite TRUE

SetTimer, runscript, -5000

return

;___________________________________________________________________________

Esc:: Exitapp ;<- use the esc key to end the script if it goes crazy