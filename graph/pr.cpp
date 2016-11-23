#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <string> 
using namespace std;

unordered_map<int, int> o2n, n2o;
int n;
vector< vector<int> > g, g_t;
vector< double > R, I;

const double lambda = 0.15;

void read_map()
{
	fstream in("vert_id.txt");
	int N; in >> N;
	for (int i = 0; i < N; i++)
	{
		int o, n; in >> o >> n;
		o2n[o] = n;
		n2o[n] = o;
	}
}

void build_graph()
{
	fstream cin("graph.txt");
	cin >> n;
	g.resize(n);
	g_t.resize(n);
	int v, u;
	while (cin >> v >> u)
	{
		g[o2n[v]].push_back(o2n[u]);
		g_t[o2n[u]].push_back(o2n[v]);
	}
}

void flush(bool old = false, const char* fname = "PR.txt")
{
	ofstream cout;
	cout.open(fname);
	for (int i = 0; i < n; i++)
	{
		if (old)	
			cout << n2o[i] << ' ' << I[i] << endl;
		else
			cout << i << ' ' << I[i] << endl;
	}
	cout.close();
}

void pagerank(int iter, int flush_freq = 1000)
{
	for (int k = 0; k < iter; k++)
	{
		for (int i = 0; i < n; i++)
			R[i] = lambda / n;
		for (int p = 0; p < n; p++)
		{
			if (g[p].size() > 0)
			{
				for (int q : g[p])
					R[q] += (1.0 - lambda) * I[p] / g[p].size();
			}
			else 
			{
				for (int q = 0; q < n; q++)
					R[q] += (1.0 - lambda) * I[p] / n;
			}
			for (int v = 0; v < n; v++)
				I[v] = R[v];

			if (p % flush_freq == 0 || p == n - 1)
				flush();
		}

		std::string fname = "PR_iter/" + std::to_string(k);
		flush(true, fname.c_str());
	}
}

void init(bool from_file = false)
{
	if (!from_file)
	{
		I.assign(n, 1.0 / n);
	}
	else 
	{
		I.resize(n);		
		fstream cin("PR.txt");
		for (int i = 0; i < n; i++)
		{
			int v; double r; cin >> v >> r;
			I[o2n[v]] = r;
		}
	}

	R.assign(n, lambda / n);
}

void check_PR(const char* fname)
{
	fstream cin(fname);
	R.assign(n, 0);
	int v; double pr;
	while (cin >> v >> pr)
	{
		R[o2n[v]] = pr;
	}

	double sum = 0;
	double min_pr = 1;
	double max_pr = -1;
	for (int i = 0; i < n; i++)
	{
		sum += R[i];
		min_pr = min(min_pr, R[i]);
		max_pr = max(max_pr, R[i]);
	}
	cout << sum << ' ' << min_pr << ' ' << max_pr << endl;

	for (int v = 0; v < n; v++)
	{
		double pr = 0;
		for (int u : g_t[v])
			pr += R[u] / g[u].size();
		cout << R[v] << ' ' << pr <<  ' ' << (1-lambda)*pr << ' ' << (1-lambda)*pr + lambda/n << endl;
		break;
	}
}

int main()
{
	read_map();
	build_graph();
	
	/*init(false);
	pagerank(5);

	flush(true);*/
	check_PR("PR_iter/4");

	return 0;
}
