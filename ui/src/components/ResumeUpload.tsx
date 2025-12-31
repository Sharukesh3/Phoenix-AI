import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Upload } from 'lucide-react'

interface Props {
  onSubmit: (file: File | null, github: string) => void
}

const ResumeUpload: React.FC<Props> = ({ onSubmit }) => {
  const [file, setFile] = useState<File | null>(null)
  const [github, setGithub] = useState('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  return (
    <Card className="w-full max-w-lg mx-auto shadow-lg">
      <CardHeader>
        <CardTitle>Build Your Profile</CardTitle>
        <CardDescription>Upload your resume or provide GitHub to get started</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
           <Label htmlFor="resume">Resume (PDF)</Label>
           <div className="flex items-center gap-2 border rounded-md p-2 bg-slate-50">
             <Upload className="text-slate-400 h-5 w-5" />
             <Input 
               id="resume" 
               type="file" 
               accept=".pdf" 
               className="border-0 bg-transparent file:bg-blue-100 file:text-blue-700 file:border-0 file:rounded-full file:px-4 file:py-1 file:text-sm hover:file:bg-blue-200"
               onChange={handleFileChange}
             />
           </div>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white px-2 text-slate-500">Or / And</span>
          </div>
        </div>

        <div className="space-y-2">
           <Label htmlFor="github">GitHub Username</Label>
           <Input 
             id="github" 
             placeholder="e.g. torvalds" 
             value={github} 
             onChange={(e) => setGithub(e.target.value)} 
           />
        </div>
      </CardContent>
      <CardFooter>
        <Button 
          className="w-full" 
          onClick={() => onSubmit(file, github)}
          disabled={!file && !github}
        >
          Analyze Profile
        </Button>
      </CardFooter>
    </Card>
  )
}

export default ResumeUpload
