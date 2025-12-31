import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

interface Props {
  onSubmit: (context: string, jobDesc: string) => void
  onBack: () => void
}

const RecoveryForm: React.FC<Props> = ({ onSubmit, onBack }) => {
  const [context, setContext] = useState('')
  const [jobDesc, setJobDesc] = useState('')

  return (
    <Card className="w-full max-w-2xl mx-auto border-red-200 bg-red-50/10">
      <CardHeader>
        <CardTitle className="text-red-700">Rejection Recovery Mode</CardTitle>
        <CardDescription>Tell us about the rejection so the Agent can diagnose the issue.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="context">What happened? (Feedback received, interview stage, etc.)</Label>
          <Textarea 
             id="context"
             placeholder="I was rejected after the system design round. They mentioned my distributed systems knowledge was weak..."
             className="min-h-[100px]"
             value={context}
             onChange={(e) => setContext(e.target.value)}
          />
        </div>
        
        <div className="space-y-2">
           <Label htmlFor="job">Job Description (Paste the content)</Label>
           <Textarea 
             id="job"
             placeholder="Senior Software Engineer - Responsibilities: ..."
             className="min-h-[150px]"
             value={jobDesc}
             onChange={(e) => setJobDesc(e.target.value)}
           />
        </div>
      </CardContent>
      <CardFooter className="flex justify-between">
         <Button variant="ghost" onClick={onBack}>Cancel</Button>
         <Button 
           className="bg-red-600 hover:bg-red-700" 
           onClick={() => onSubmit(context, jobDesc)}
           disabled={!context || !jobDesc}
         >
           Generate Recovery Strategy
         </Button>
      </CardFooter>
    </Card>
  )
}

export default RecoveryForm
