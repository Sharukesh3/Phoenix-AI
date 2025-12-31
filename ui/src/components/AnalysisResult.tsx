import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import ReactMarkdown from 'react-markdown'
import { ScrollArea } from '@/components/ui/scroll-area'

interface AnalysisData {
  resume_data: any
  github_data: any
  skills: any
}

const AnalysisResult: React.FC<{ data: any }> = ({ data }) => {
  // Handle nested structure from FastAPI AnalysisResponse
  const profile_summary = data.profile_summary || {};
  const resume = profile_summary.resume_data || {};
  const github = data.github_stats || profile_summary.github_data || {};
  const extractedSkills = data.skills?.technical_skills || profile_summary.skills?.technical_skills || {};

  return (
    <div className="space-y-6">
      <Card className="shadow-md border-t-4 border-t-blue-500">
        <CardHeader>
          <CardTitle className="text-xl text-blue-900">Profile Analysis</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
           {/* Profile Summary */}
           <div className="prose prose-sm max-w-none text-slate-700">
             <p className="font-medium">
               {resume.raw_text ? `Analyzed resume for ${resume.contact_info?.name || 'Candidate'}` : 'No resume text analyzed.'}
             </p>
             {github.bio && <div className="mt-2 p-3 bg-slate-50 rounded-md italic text-slate-600"><ReactMarkdown>{github.bio}</ReactMarkdown></div>}
           </div>

           {/* GitHub Stats */}
           {github.username && !github.error && (
             <div className="mt-6 border-t pt-4">
               <h3 className="font-bold text-lg mb-3 flex items-center gap-2">
                 <span className="text-xl">📦</span> GitHub Profile Analysis
               </h3>
               <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg">
                  <div>
                    <p><strong>Username:</strong> {github.username}</p>
                    <p><strong>Public Repos:</strong> {github.public_repos}</p>
                    <p><strong>Followers:</strong> {github.followers}</p>
                  </div>
                  <div>
                    <p className="font-semibold mb-1">Top Languages:</p>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(github.languages || {}).slice(0, 6).map(([lang, pct]: any) => (
                        <Badge key={lang} variant="secondary" className="text-xs">
                          {lang}: {pct}%
                        </Badge>
                      ))}
                    </div>
                  </div>
               </div>
               
               {/* Activity Metrics */}
               {github.activity_metrics && (
                  <div className="mt-4 grid grid-cols-3 gap-2 text-center">
                    <div className="bg-white p-2 rounded border shadow-sm">
                      <p className="text-xs text-slate-500 uppercase tracking-wider">Stars</p>
                      <p className="font-bold text-xl">{github.activity_metrics.total_stars}</p>
                    </div>
                    <div className="bg-white p-2 rounded border shadow-sm">
                      <p className="text-xs text-slate-500 uppercase tracking-wider">Forks</p>
                      <p className="font-bold text-xl">{github.activity_metrics.total_forks}</p>
                    </div>
                     <div className="bg-white p-2 rounded border shadow-sm">
                      <p className="text-xs text-slate-500 uppercase tracking-wider">Commits (Est)</p>
                      <p className="font-bold text-xl">{github.public_repos * 30 + 20}+</p>
                    </div>
                  </div>
               )}
               
               {/* Top Repos */}
               {github.top_repos && github.top_repos.length > 0 && (
                   <div className="mt-4">
                       <h4 className="text-sm font-semibold mb-2">⭐ Top Repositories</h4>
                       <ul className="space-y-2">
                           {github.top_repos.slice(0, 3).map((repo: any) => (
                               <li key={repo.name} className="flex justify-between items-center text-sm bg-white p-2 rounded border">
                                   <a href={repo.url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline font-medium">
                                       {repo.name}
                                   </a>
                                   <span className="text-xs text-slate-500">⭐ {repo.stars} | {repo.language}</span>
                               </li>
                           ))}
                       </ul>
                   </div>
               )}
             </div>
           )}

           {/* Categorized Skills */}
           <div className="mt-6 border-t pt-4">
            <h3 className="font-bold text-lg mb-3 text-slate-800">🛠️ Skills Extracted from Resume</h3>
            <ScrollArea className="h-[400px] w-full rounded-md border p-4 bg-slate-50">
                <div className="space-y-6">
                  {Object.entries(extractedSkills).map(([category, items]: any) => (
                    <div key={category}>
                      <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider mb-2">{category.replace(/_/g, ' ')}</h4>
                      <div className="flex flex-wrap gap-2">
                        {Array.isArray(items) && items.map((skill: any, idx: number) => {
                          const name = Array.isArray(skill) ? skill[0] : skill;
                          return (
                            <Badge key={idx} variant="outline" className="bg-white border-slate-300 text-slate-700">
                              {name}
                            </Badge>
                          )
                        })}
                        {(!items || items.length === 0) && <span className="text-sm text-slate-400 italic">None detected</span>}
                      </div>
                    </div>
                  ))}
                  {Object.keys(extractedSkills).length === 0 && <p className="text-slate-500 italic">No skills extracted yet.</p>}
                </div>
            </ScrollArea>
           </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AnalysisResult
