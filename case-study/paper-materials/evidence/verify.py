"""Audit the preserved experiment subset offline; no external packages required."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
NS = {'g': 'http://graphml.graphdrawing.org/xmlns'}
EXPECTED = {
    'baseline': ('30d8786ed35582a772f8fdba44918a844b85f45b', 1074, 516, 'PASSED', 0),
    'violation': ('b9cf2ac13b5bc573386c02294bdb60f50e0a114c', 1077, 517, 'FAILED', 1),
    'repair': ('3bce90dfb2cbffeb94b5cb90e76871b44c9dedc4', 1074, 516, 'PASSED', 0),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    for line in (HERE.parent / 'CHECKSUMS.sha256').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(hashlib.sha256((HERE.parent / name).read_bytes()).hexdigest() == digest,
                'Checksum mismatch: ' + name)
    provenance = json.loads((HERE / 'provenance.json').read_text())
    membership = json.loads((HERE.parent / 'component-membership.json').read_text())
    require({k: len(v) for k, v in membership.items()} ==
            {'Expression API': 24, 'Common utilities': 5, 'SpEL implementation': 115},
            'Component counts differ')
    expected_nodes = {n for members in membership.values() for n in members}
    require(sum(map(len, membership.values())) == len(expected_nodes), 'Duplicate membership')
    graphs = {}
    for stage, (sha, passed, edge_count, verdict, violations) in EXPECTED.items():
        folder = HERE / stage
        result = json.loads((folder / 'dcode-result.json').read_text())
        gate = result['architecture_gate']
        require(result['commit'] == sha == provenance[stage]['commit'], stage + ': commit mismatch')
        require(gate['is_active'] is True and gate['result'] == verdict, stage + ': gate mismatch')
        require(gate['details'] == {'totalViolations': violations, 'totalWarnings': 0,
                                   'totalEdgesAnalyzed': edge_count}, stage + ': gate details mismatch')
        tree = ET.parse(folder / 'DependencyGraph.graphml')
        nodes = {n.attrib['id'] for n in tree.findall('.//g:node', NS)}
        edges = {(e.attrib['source'], e.attrib['target']) for e in tree.findall('.//g:edge', NS)}
        require(nodes == expected_nodes and len(edges) == edge_count, stage + ': graph mismatch')
        graphs[stage] = edges
        totals = dict.fromkeys(['tests', 'failures', 'errors', 'skipped'], 0)
        with zipfile.ZipFile(folder / 'junit-xml.zip') as archive:
            require(set(archive.namelist()) == set(provenance[stage]['junit_xml_sha256']),
                    stage + ': XML file list mismatch')
            for name in archive.namelist():
                data = archive.read(name)
                require(hashlib.sha256(data).hexdigest() == provenance[stage]['junit_xml_sha256'][name],
                        stage + ': XML hash mismatch: ' + name)
                suite = ET.fromstring(data)
                for key in totals:
                    totals[key] += int(suite.attrib.get(key, 0))
        totals['passed'] = totals['tests'] - totals['failures'] - totals['errors'] - totals['skipped']
        require(totals == {'tests': passed + 11, 'failures': 0, 'errors': 0, 'skipped': 11,
                           'passed': passed}, stage + ': test result mismatch')
        require(totals == provenance[stage]['functional_tests'], stage + ': provenance totals mismatch')
        print(f'{stage}: {passed} passed, 11 skipped, 144 nodes, {edge_count} edges, gate {verdict}')
    prefix = 'org.springframework.expression.'
    introduced = (prefix + 'common.ExpressionUtils', prefix + 'spel.standard.SpelExpressionParser')
    require(graphs['violation'] - graphs['baseline'] == {introduced}, 'Unexpected added edges')
    require(not graphs['baseline'] - graphs['violation'], 'Unexpected removed edges')
    require(graphs['repair'] == graphs['baseline'], 'Repair differs from baseline')
    for edge in [(prefix + 'spel.standard.SpelExpressionParser', prefix + 'spel.standard.SpelExpression'),
                 (prefix + 'spel.standard.SpelExpression', prefix + 'common.ExpressionUtils'),
                 (prefix + 'common.ExpressionUtils', prefix + 'TypeConverter')]:
        require(edge in graphs['baseline'], 'Missing depicted baseline edge: ' + str(edge))
    print('Verified: one introduced edge, existing return path, unchanged membership, exact repair edge set.')


if __name__ == '__main__':
    main()
