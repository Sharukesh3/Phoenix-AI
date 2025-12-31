from github import Github
from typing import Dict, List, Any
import os

class GitHubAnalyzer:
    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.github = Github(self.token) if self.token else None

    def analyze_user(self, username: str) -> Dict[str, Any]:
        if not self.github:
            return {'error': 'GitHub token not provided'}
            
        try:
            user = self.github.get_user(username)
            repos = list(user.get_repos())

            languages = self._get_languages(repos)
            activity_metrics = self._get_activity_metrics(repos)
            top_repos = self._get_top_repos(repos)

            return {
                'username': username,
                'name': user.name,
                'bio': user.bio,
                'public_repos': user.public_repos,
                'followers': user.followers,
                'following': user.following,
                'languages': languages,
                'activity_metrics': activity_metrics,
                'top_repos': top_repos
            }
        except Exception as e:
            return {'error': str(e)}

    def _get_languages(self, repos) -> Dict[str, int]:
        languages = {}
        for repo in repos:
            try:
                repo_languages = repo.get_languages()
                for lang, bytes_count in repo_languages.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except: pass

        total = sum(languages.values())
        if total > 0:
            languages = {lang: round((count / total) * 100, 2) for lang, count in languages.items()}

        return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))

    def _get_activity_metrics(self, repos) -> Dict[str, Any]:
        total_stars = 0
        total_forks = 0

        for repo in repos:
            total_stars += repo.stargazers_count
            total_forks += repo.forks_count

        return {
            'total_stars': total_stars,
            'total_forks': total_forks
        }

    def _get_top_repos(self, repos, limit=5) -> List[Dict[str, Any]]:
        sorted_repos = sorted(repos, key=lambda r: r.stargazers_count, reverse=True)[:limit]

        top_repos = []
        for repo in sorted_repos:
            top_repos.append({
                'name': repo.name,
                'description': repo.description,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'language': repo.language,
                'url': repo.html_url
            })

        return top_repos
