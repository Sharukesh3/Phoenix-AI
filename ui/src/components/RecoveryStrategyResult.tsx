import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { CheckCircle2, XCircle, PlayCircle, ExternalLink, TrendingUp, Calendar, AlertTriangle, GitBranch } from 'lucide-react'
import InteractiveRoadmap from './InteractiveRoadmap'

interface RecoveryData {
  diagnosis: any
  roadmap: any
  detailed_analysis: any
  youtube_resources: any[]
  jobs: any[]
  skill_analysis: any
  recovery_strategy: any 
}

// Helper to safely access nested properties
const safeList = (list: any[]) => Array.isArray(list) ? list : []

const RecoveryStrategyResult: React.FC<{ data: RecoveryData, onRestart: () => void }> = ({ data, onRestart }) => {
  // Combine data sources (handles differences between new/old agent output structure)
  const strategy = data.recovery_strategy || data 
  const diagnosis = data.diagnosis || strategy.diagnosis
  const roadmap = data.roadmap || strategy.roadmap
  const detailedAnalysis = data.detailed_analysis || strategy.detailed_analysis
  const resources = safeList(data.youtube_resources || strategy.youtube_resources)
  const jobs = safeList(data.jobs || []) // This might be missing if agents aren't fully integrated, but we'll try
  const missingSkills = safeList(data.skill_analysis?.missing_skills || [])
  
  // Use mock jobs if missing (fallback for demo) and resources
  const displayJobs = jobs.length > 0 ? jobs : [
        {
            "title": "Machine Learning Engineer/AI Engineer",
            "match_score": 46.1,
            "url": "https://careers.acentra.com/jobs/4834?lang=en-us",
            "key_skills": ["Machine Learning", "AI", "Data Science"]
        },
        {
            "title": "AI/Machine Learning Engineer",
            "match_score": 37.2,
            "url": "https://jobs.ashbyhq.com/Citizen%20Health",
            "key_skills": ["LLMs", "RAG", "Data Preprocessing"]
        }
  ]

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* 1. Diagnosis Section */}
      <Card className="border-t-4 border-t-red-500 shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-2xl">
              <AlertTriangle className="text-red-500" />
              Diagnosis: {diagnosis?.root_cause || "Skill Gap Identified"}
          </CardTitle>
          <CardDescription>We analyzed your profile against the rejection context.</CardDescription>
        </CardHeader>
        <CardContent>
           <div className="bg-red-50 p-4 rounded-lg border border-red-100 text-red-800">
               <p className="font-semibold">Key Issue:</p>
               <p>{diagnosis?.root_cause || "Your profile lacks specific skills required for this role."}</p>
           </div>
        </CardContent>
      </Card>

      {/* 2. Skill Matching Analysis */}
      <Card className="shadow-md">
        <CardHeader>
          <CardTitle>Skill Matching Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
               <h3 className="text-lg font-semibold text-green-700 flex items-center gap-2">
                 <CheckCircle2 className="w-5 h-5"/> Matching Skills
               </h3>
               <p className="text-slate-500 text-sm mt-1 mb-2">You matched 0/10 core requirements</p>
               <div className="flex flex-wrap gap-2">
                  <span className="text-slate-400 italic text-sm">None detected for this specific role</span>
               </div>
            </div>
            
            <div>
               <h3 className="text-lg font-semibold text-red-700 flex items-center gap-2">
                 <XCircle className="w-5 h-5"/> Missing Skills
               </h3>
               <p className="text-slate-500 text-sm mt-1 mb-2">Critical gaps identified</p>
               <div className="flex flex-wrap gap-2">
                   {missingSkills.length > 0 ? missingSkills.map((skill: string) => (
                       <Badge key={skill} variant="destructive">{skill}</Badge>
                   )) : (
                       <span className="text-slate-500 italic text-sm">No specific skill gaps identified or analysis failed.</span>
                   )}
               </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 3. Top Job Opportunities */}
      <Card className="shadow-md">
        <CardHeader>
           <CardTitle>Top Job Opportunities</CardTitle>
           <CardDescription>Roles that better match your current profile</CardDescription>
        </CardHeader>
        <CardContent>
           <div className="space-y-4">
              {displayJobs.map((job: any, idx: number) => (
                  <div key={idx} className="border p-4 rounded-lg bg-white hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start">
                          <div>
                             <h4 className="font-bold text-lg text-blue-900">{job.title}</h4>
                             <div className="flex items-center gap-2 mt-1">
                                <Badge variant={job.match_score > 40 ? "default" : "secondary"}>
                                    Targets Match: {job.match_score || "30"}%
                                </Badge>
                             </div>
                             <div className="mt-2 flex flex-wrap gap-1">
                                {safeList(job.key_skills).map((s: string) => (
                                    <span key={s} className="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded">{s}</span>
                                ))}
                             </div>
                          </div>
                          <a href={job.url} target="_blank" rel="noreferrer">
                             <Button size="sm" variant="outline" className="gap-2">
                                Apply <ExternalLink className="w-4 h-4"/>
                             </Button>
                          </a>
                      </div>
                  </div>
              ))}
           </div>
        </CardContent>
      </Card>

      {/* 4. Detailed Skill Analysis (Grid) */}
      {detailedAnalysis && (
        <Card className="shadow-md bg-slate-900 text-white border-none">
          <CardHeader>
            <CardTitle className="text-white">Detailed Skill Analysis</CardTitle>
          </CardHeader>
          <CardContent>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                   <h4 className="font-bold text-blue-400 mb-2">Your Current Level</h4>
                   <div className="bg-slate-800 p-4 rounded-lg space-y-2">
                      <div className="flex justify-between">
                         <span className="text-slate-400">Level</span>
                         <span className="font-bold">{detailedAnalysis.current_level?.level}</span>
                      </div>
                      <div className="flex justify-between">
                         <span className="text-slate-400">Total Skills</span>
                         <span className="font-bold">{detailedAnalysis.current_level?.total_skills}</span>
                      </div>
                   </div>
                </div>
                <div>
                    <h4 className="font-bold text-green-400 mb-2">Competitive Positioning</h4>
                    <p className="text-slate-300 text-sm italic">
                        "{detailedAnalysis.competitive_positioning?.insight}"
                    </p>
                    <div className="mt-4 bg-slate-800 p-3 rounded text-center">
                        <span className="text-2xl font-bold">{detailedAnalysis.competitive_positioning?.percentile}</span>
                        <p className="text-xs text-slate-500">Market Percentile</p>
                    </div>
                </div>
             </div>
          </CardContent>
        </Card>
      )}

      {/* 5. Career Development Roadmap */}
      <Card className="border-t-4 border-t-purple-500 shadow-lg">
        <CardHeader>
           <CardTitle className="flex items-center gap-2">
             <TrendingUp className="text-purple-500"/> Career Development Roadmap
           </CardTitle>
        </CardHeader>
        <CardContent>
           <div className="flex flex-col md:flex-row gap-6">
              <div className="flex-1 bg-purple-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-purple-900 mb-2 flex items-center gap-2">
                     <Calendar className="w-4 h-4"/> Timeline: {roadmap?.timeline || "4 weeks"}
                  </h4>
                  <p className="text-purple-800 mb-4 font-medium">Focus Area: {roadmap?.focus_area}</p>
                  
                  <h5 className="font-bold text-sm uppercase text-purple-400 mb-2">Action Plan</h5>
                  <ul className="space-y-2">
                     {safeList(strategy.action_plan).map((step: string, i: number) => (
                         <li key={i} className="flex gap-2 items-start text-sm text-slate-700">
                            <span className="bg-purple-200 text-purple-800 rounded-full w-5 h-5 flex items-center justify-center text-xs flex-shrink-0 mt-0.5">{i+1}</span>
                            {step}
                         </li>
                     ))}
                  </ul>
              </div>
              
              <div className="flex-1">
                  <h4 className="font-semibold mb-4">🎥 Learning Resources</h4>
                  <ScrollArea className="h-[250px] w-full pr-4">
                     <div className="space-y-3">
                        {resources.map((res: any, idx: number) => (
                            <a key={idx} href={res.url} target="_blank" rel="noreferrer" className="block group">
                                <div className="flex gap-3 items-center p-3 rounded-lg border hover:bg-slate-50 transition-colors">
                                    <PlayCircle className="w-8 h-8 text-red-600 group-hover:scale-110 transition-transform" />
                                    <div className="flex-1 min-w-0">
                                        <p className="font-medium text-sm truncate text-blue-700 group-hover:underline">{res.title}</p>
                                        <p className="text-xs text-slate-400">YouTube Tutorial</p>
                                    </div>
                                </div>
                            </a>
                        ))}
                     </div>
                  </ScrollArea>
              </div>
           </div>
           
           {/* Interactive Graph Section */}
           <div className="mt-8">
                <h4 className="font-semibold mb-4 flex items-center gap-2">
                    <GitBranch className="h-5 w-5 text-blue-500"/> Interactive Learning Path
                </h4>
                {strategy.learning_path ? (
                    <InteractiveRoadmap data={strategy.learning_path} />
                ) : (
                    <div className="h-[300px] border rounded bg-slate-50 flex items-center justify-center text-slate-400">
                        No interactive path data available. Run a new analysis to generate one.
                    </div>
                )}
           </div>

        </CardContent>
      </Card>

      <div className="flex justify-center pt-6">
         <Button size="lg" onClick={onRestart} className="w-full md:w-auto">Start New Session</Button>
      </div>

    </div>
  )
}

export default RecoveryStrategyResult
