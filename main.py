from manager.agent_manager import AgentManager
from memory.miras_memory import MIRASMemory
import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <resume_path> [job_description_file]")
        print("Example: python main.py resume.pdf job_description.txt")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    job_description_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    job_description = ""
    if job_description_file:
        with open(job_description_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
    
    print("="*80)
    print("CAREER INTELLIGENCE SYSTEM - PHASE 2")
    print("="*80)
    print(f"\nResume: {resume_path}")
    if job_description_file:
        print(f"Job Description: {job_description_file}")
    print("\n" + "="*80 + "\n")
    
    memory = MIRASMemory()
    manager = AgentManager(memory=memory)
    
    print("Step 1: Analyzing Profile...")
    print("-" * 80)
    
    result = manager.execute_workflow(
        user_request="Analyze profile, find matching jobs, and provide career guidance",
        resume_path=resume_path,
        job_query="AI Engineer LLM RAG Machine Learning jobs",
        job_description_file=job_description_file,
        rejection_scenario=bool(job_description),
        rejected_job={
            'title': 'Target Position',
            'content': job_description,
            'required_skills': []
        } if job_description else {},
        rejection_context="Analyzing fit for target position"
    )
    
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80 + "\n")
    
    print("=" * 80)
    print("PROFILE ANALYSIS")
    print("=" * 80)
    print(result.get('profile_summary', 'N/A'))
    print()
    
    if result.get('github_data'):
        github = result['github_data']
        print("\n" + "=" * 80)
        print("GITHUB PROFILE ANALYSIS")
        print("=" * 80)
        if github.get('username'):
            print(f"\n👤 Username: {github['username']}")
        if github.get('public_repos'):
            print(f"📦 Public Repos: {github['public_repos']}")
        if github.get('followers'):
            print(f"👥 Followers: {github['followers']}")
        
        if github.get('languages'):
            print(f"\n💻 TOP LANGUAGES:")
            for lang, pct in list(github['languages'].items())[:8]:
                print(f"   • {lang}: {pct}%")
        
        if github.get('activity_metrics'):
            metrics = github['activity_metrics']
            print(f"\n📊 ACTIVITY METRICS:")
            print(f"   • Total Commits: {metrics.get('total_commits', 0)}")
            print(f"   • Total Stars: {metrics.get('total_stars', 0)}")
            print(f"   • Total Forks: {metrics.get('total_forks', 0)}")
        
        if github.get('top_repos'):
            print(f"\n⭐ TOP REPOSITORIES:")
            for repo in github['top_repos'][:5]:
                print(f"   • {repo['name']} ({repo['language']}) - ⭐ {repo['stars']}")
    
    if result.get('extracted_skills'):
        print("\n" + "=" * 80)
        print("SKILLS EXTRACTED FROM RESUME")
        print("=" * 80)
        skills = result['extracted_skills']
        for category, skill_list in skills.items():
            if skill_list:
                print(f"\n{category.upper().replace('_', ' ')}:")
                for skill, score in skill_list[:10]:
                    print(f"   • {skill} (proficiency: {score})")
    
    if result.get('skill_match_analysis'):
        skill_analysis = result['skill_match_analysis']
        print("\n" + "=" * 80)
        print("SKILL MATCHING ANALYSIS")
        print("=" * 80)
        print(f"\n📊 Overall Match: {skill_analysis['match_percentage']}%")
        print(f"✅ Matching Skills: {skill_analysis['total_matching']}/{skill_analysis['total_required']}")
        print(f"❌ Missing Skills: {skill_analysis['total_missing']}")
        
        if skill_analysis.get('matching_skills'):
            print(f"\n✅ YOUR MATCHING SKILLS ({len(skill_analysis['matching_skills'])}):")
            for skill in skill_analysis['matching_skills']:
                print(f"   • {skill}")
        
        if skill_analysis.get('missing_skills'):
            print(f"\n❌ SKILLS YOU NEED TO LEARN ({len(skill_analysis['missing_skills'])}):")
            for skill in skill_analysis['missing_skills'][:10]:
                print(f"   • {skill}")
    
    if result.get('top_jobs'):
        print("\n\n" + "=" * 80)
        print(f"TOP JOB OPPORTUNITIES ({len(result['top_jobs'])} FOUND)")
        print("=" * 80)
        for idx, job in enumerate(result['top_jobs'][:10], 1):
            print(f"\n{idx}. {job['title']}")
            print(f"   🎯 Match Score: {job['match_score']:.1%}")
            print(f"   🔗 Apply: {job['url']}")
            if job.get('required_skills'):
                print(f"   💼 Key Skills: {', '.join(job['required_skills'][:5])}")
    else:
        print("\n\n" + "=" * 80)
        print("JOB OPPORTUNITIES")
        print("=" * 80)
        print("\n⚠️  No jobs found in search. Searching alternative sources...")
        print("\nRecommended Job Boards:")
        print("   • LinkedIn: https://www.linkedin.com/jobs/search/?keywords=AI%20Engineer")
        print("   • Indeed: https://www.indeed.com/jobs?q=AI+Engineer")
        print("   • Glassdoor: https://www.glassdoor.com/Job/ai-engineer-jobs-SRCH_KO0,11.htm")
        print("   • AngelList: https://angel.co/jobs (for startups)")
    
    if result.get('recovery_plan'):
        print("\n\n" + "=" * 80)
        print("CAREER DEVELOPMENT ROADMAP")
        print("=" * 80)
        plan = result['recovery_plan']
        print(f"\n🎯 Focus Area: {plan['root_cause']}")
        print(f"⏱️  Timeline: {plan['timeline']}")
        
        if plan.get('priority_actions'):
            print("\n📋 ACTION PLAN:")
            for idx, action in enumerate(plan['priority_actions'], 1):
                print(f"\n   {idx}. {action.get('action', 'N/A')}")
                print(f"      → {action.get('description', 'N/A')}")
        
        if plan.get('resources'):
            print("\n\n📚 LEARNING RESOURCES:")
            for skill, resources in list(plan['resources'].items())[:5]:
                print(f"\n   {skill}:")
                for resource in resources[:4]:
                    print(f"      • {resource}")
        
        if plan.get('detailed_timeline'):
            timeline_detail = plan['detailed_timeline']
            print("\n\n📅 DETAILED LEARNING TIMELINE:")
            print(f"   Total Duration: {timeline_detail['total_weeks']} weeks\n")
            
            for week_name, week_data in timeline_detail['weekly_breakdown'].items():
                print(f"   {week_name}:")
                print(f"      Focus: {', '.join(week_data['focus_skills'])}")
                print(f"      Time: {week_data['time_commitment']}")
                if week_data.get('deliverables'):
                    print(f"      Deliverable: {week_data['deliverables'][0]}")
                print()
            
            print(f"   🎯 Final Project: {timeline_detail['final_project']}")
            print(f"\n   ✅ Success Metrics:")
            for metric in timeline_detail['success_metrics']:
                print(f"      • {metric}")
    
    if result.get('detailed_analysis'):
        analysis = result['detailed_analysis']
        print("\n\n" + "=" * 80)
        print("DETAILED SKILL ANALYSIS")
        print("=" * 80)
        
        your_level = analysis['your_level']
        print(f"\n🎯 YOUR CURRENT LEVEL: {your_level['level']} ({your_level['overall_rating']}/10)")
        print(f"   • Total Skills: {your_level['total_skills']}")
        print(f"   • GitHub Commits: {your_level['github_activity']}")
        print(f"   • GitHub Repos: {your_level['github_repos']}")
        
        if your_level.get('strengths'):
            print(f"\n💪 YOUR STRENGTHS:")
            for strength in your_level['strengths']:
                print(f"   • {strength}")
        
        industry = analysis['industry_expectations']
        print(f"\n\n🏢 INDUSTRY EXPECTATIONS:")
        print(f"   • Expected Level: {industry['expected_level']}")
        print(f"   • Experience: {industry['years_experience']}")
        print(f"   • Must-Have Skills: {', '.join(industry['must_have_skills'])}")
        
        gap = analysis['gap_analysis']
        if gap.get('critical_gaps'):
            print(f"\n\n🚨 CRITICAL SKILL GAPS:")
            for skill in gap['critical_gaps']:
                print(f"   • {skill}")
        
        if gap.get('github_improvement_areas'):
            print(f"\n📈 GITHUB IMPROVEMENT AREAS:")
            for area in gap['github_improvement_areas']:
                print(f"   • {area}")
        
        competitive = analysis['competitive_analysis']
        print(f"\n\n📊 COMPETITIVE POSITIONING:")
        print(f"   • Market Percentile: Top {100 - competitive['market_percentile']}%")
        print(f"   • {competitive['recommendation']}")
    
    if result.get('youtube_tutorials'):
        tutorials = result['youtube_tutorials']
        print("\n\n" + "=" * 80)
        print("🎥 YOUTUBE LEARNING RESOURCES")
        print("=" * 80)
        print(f"\nFound {len(tutorials)} skill-specific tutorial playlists:\n")
        
        for skill, videos in tutorials.items():
            print(f"📚 {skill}:")
            for video in videos:
                print(f"   • {video['title']}")
                print(f"     🔗 {video['url']}")
            print()
    
    print("\n" + "=" * 80)
    print("MIRAS MEMORY SYSTEM")
    print("=" * 80)
    stats = result.get('memory_stats', {})
    print(f"💾 Total Insights Retained: {stats.get('total_memories', 0)}")
    print(f"🎲 Avg Novelty Score: {stats.get('avg_novelty', 0):.3f}")
    print(f"🔄 Avg Access Count: {stats.get('avg_access_count', 0):.2f}")
    
    print("\n" + "="*80)
    print("WORKFLOW COMPLETE")
    print("="*80)
    
    memory.save_to_file('memory_storage.json')
    print("\nMemory saved to: memory_storage.json")

if __name__ == "__main__":
    main()
