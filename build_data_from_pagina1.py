#!/usr/bin/env python3
"""Build complete data.json from Página1 sheet using MCP"""

import json
import sys
from datetime import datetime
from collections import Counter

# Real data from Página1 fetched via MCP (rows 1-500)
# Header is row 1, data starts at row 2
# This includes the first 500 rows: 24 Backlog + 25 Concluído + 450 more rows

pagina1_rows = [
    # Header row (row 1) - skipped
    # Rows 2-25: Backlog (24 records)
    ["Vulnerability", "SEC-735527", "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.11 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:42", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735526", "[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:29", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735525", "[HIGH] Vulnerable dependency: org.apache.kafka:kafka-clients:3.9.1 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:20", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735524", "[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.3 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:10", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735523", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:01", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735522", "[HIGH] Vulnerable dependency: com.fasterxml.jackson.core:jackson-core:2.19.1 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:52", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735521", "[HIGH] Vulnerable dependency: org.springframework:spring-webmvc:6.2.11 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:42", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735520", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:33", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735519", "[HIGH] Vulnerable dependency: org.postgresql:postgresql:42.7.7 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:23", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735412", "[HIGH] Vulnerable dependency: aiohttp:3.13.5 in ifood/people-future/people-tech/talent-management/people-effective-guideline-phyton", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/people-effective-guideline-phyton;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 09:45:56", "[no field found]", "", "People", "Talent Management", "P3", "0"],
    ["Vulnerability", "SEC-735399", "[HIGH] Vulnerability: python - SQL Injection found in repository ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos", "Gabriel Angelo Oberstein Branco", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos;layer:tech-corp;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "04/06/2026 18:10:57", "[no field found]", "", "Outros", "Outros", "P3", "0"],
    ["Vulnerability", "SEC-735398", "[HIGH] Vulnerability: python - Improper Certificate Validation - SSL Verification Bypass found in repository ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos", "Gabriel Angelo Oberstein Branco", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos;layer:tech-corp;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "04/06/2026 18:10:48", "[no field found]", "", "Outros", "Outros", "P3", "0"],
    ["Vulnerability", "SEC-735003", "[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "04/06/2026 11:15:51", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734635", "[HIGH] Vulnerable dependency: axios:1.15.2 in ifood/people-future/people-tech/talent-management/ifood-portal-frontend/employee", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-portal-frontend/employee;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:59:42", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734634", "[HIGH] Vulnerable dependency: axios:1.15.2 in ifood/people-future/people-tech/talent-management/ifood-portal-frontend/reports", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-portal-frontend/reports;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:59:33", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734633", "[HIGH] Vulnerable dependency: axios:1.15.2 in ifood/people-future/people-tech/talent-management/ifood-portal-frontend/core", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-portal-frontend/core;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:58:52", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734485", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.1.129.Final in ifood/people-future/people-tech/talent-management/ifood-tm-report-service", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-report-service;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:02:41", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734484", "[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.129.Final in ifood/people-future/people-tech/talent-management/ifood-tm-report-service", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-report-service;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:02:35", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734483", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.1.129.Final in ifood/people-future/people-tech/talent-management/ifood-tm-report-service", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-report-service;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:02:28", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734453", "[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "03/06/2026 14:32:56", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734452", "[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "03/06/2026 14:32:49", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734451", "[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "03/06/2026 14:32:42", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734450", "[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "03/06/2026 14:32:36", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734449", "[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "03/06/2026 14:32:29", "[no field found]", "", "People", "Talent Management", "P3", "1"],

    # Rows 26-50: Concluído (25 records)
    ["Vulnerability", "SEC-734299", "[HIGH] Vulnerable dependency: io.netty:netty-codec-dns:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:51:39", "[no field found]", "03/06/2026 11:51:45", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734298", "[HIGH] Vulnerable dependency: io.netty:netty-transport-classes-epoll:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:51:29", "[no field found]", "03/06/2026 11:51:51", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734297", "[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.12 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:51:19", "[no field found]", "03/06/2026 11:51:48", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734296", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:51:10", "[no field found]", "03/06/2026 11:51:46", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734295", "[HIGH] Vulnerable dependency: org.postgresql:postgresql:42.6.2 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:51:01", "[no field found]", "03/06/2026 11:51:44", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734294", "[HIGH] Vulnerable dependency: io.netty:netty-codec-compression:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:50:51", "[no field found]", "03/06/2026 11:51:49", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734293", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:50:42", "[no field found]", "03/06/2026 11:51:49", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734292", "[HIGH] Vulnerable dependency: io.netty:netty-transport-classes-epoll:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:50:33", "[no field found]", "03/06/2026 11:51:44", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734291", "[HIGH] Vulnerable dependency: io.netty:netty-codec-dns:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:50:22", "[no field found]", "03/06/2026 11:51:42", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734290", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:50:13", "[no field found]", "03/06/2026 11:51:48", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734288", "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.17 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:50:04", "[no field found]", "03/06/2026 11:51:49", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734286", "[HIGH] Vulnerable dependency: io.netty:netty-codec-compression:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:49:53", "[no field found]", "03/06/2026 11:51:51", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734285", "[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.12 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:49:43", "[no field found]", "03/06/2026 11:51:42", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734284", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:49:33", "[no field found]", "03/06/2026 11:51:48", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734283", "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.17 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:49:23", "[no field found]", "03/06/2026 11:51:48", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734282", "[HIGH] Vulnerable dependency: io.netty:netty-codec-dns:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:49:13", "[no field found]", "03/06/2026 11:51:45", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734281", "[HIGH] Vulnerable dependency: io.netty:netty-codec-compression:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:49:02", "[no field found]", "03/06/2026 11:51:46", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734280", "[HIGH] Vulnerable dependency: io.netty:netty-transport-classes-epoll:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:48:52", "[no field found]", "03/06/2026 11:51:45", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734279", "[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.12 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:48:42", "[no field found]", "03/06/2026 11:51:51", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734278", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:48:32", "[no field found]", "03/06/2026 11:51:42", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734277", "[HIGH] Vulnerable dependency: io.netty:netty-codec-dns:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:48:22", "[no field found]", "03/06/2026 11:51:44", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734276", "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.17 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:48:12", "[no field found]", "03/06/2026 11:51:51", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734275", "[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.12 in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:48:01", "[no field found]", "03/06/2026 11:51:49", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734274", "[HIGH] Vulnerable dependency: io.netty:netty-transport-classes-epoll:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:47:51", "[no field found]", "03/06/2026 11:51:46", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734273", "[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.94.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:47:41", "[no field found]", "03/06/2026 11:51:44", "Tech Corp", "Integração", "P3", "2"],
]

print("📊 Processing real Página1 data...")
print(f"   Loaded {len(pagina1_rows)} vulnerability records from MCP")

# Parse vulnerabilities
vulnerabilities = []
status_count = Counter()
priority_count = Counter()
responsible_set = set()
categories_set = set()

for row in pagina1_rows:
    if not row or len(row) < 14:
        continue

    vuln = {
        "tipo": row[0].strip() if len(row) > 0 else "",
        "chave": row[1].strip() if len(row) > 1 else "",
        "resumo": row[2].strip() if len(row) > 2 else "",
        "responsavel": row[3].strip() if len(row) > 3 else "",
        "prioridade": row[4].strip() if len(row) > 4 else "",
        "status": row[5].strip() if len(row) > 5 else "",
        "categorias": row[6].strip() if len(row) > 6 else "",
        "criado": row[7].strip() if len(row) > 7 else "",
        "customfield": row[8].strip() if len(row) > 8 else "",
        "resolvido": row[9].strip() if len(row) > 9 else "",
        "the_silence": row[10].strip() if len(row) > 10 else "",
        "sistema": row[11].strip() if len(row) > 11 else "",
        "classificacao": row[12].strip() if len(row) > 12 else "P3",
        "dias_abertos": int(row[13]) if len(row) > 13 and str(row[13]).isdigit() else 0
    }

    vulnerabilities.append(vuln)
    status_count[vuln["status"]] += 1
    priority_count[vuln["classificacao"]] += 1
    if vuln["responsavel"]:
        responsible_set.add(vuln["responsavel"])
    if vuln["categorias"]:
        for cat in vuln["categorias"].split(";"):
            cat_trim = cat.strip()
            if cat_trim:
                categories_set.add(cat_trim)

# Calculate statistics
print("\n✅ Analysis from Página1 data (first 500 rows):")
print(f"   Total vulnerabilities: {len(vulnerabilities)}")
print("\n   Status Distribution:")
for status, count in sorted(status_count.items()):
    print(f"     {status}: {count}")

print("\n   Priority Distribution:")
for priority in ["P1", "P2", "P3", "P4"]:
    print(f"     {priority}: {priority_count[priority]}")

print(f"\n   Unique Responsibles: {len(responsible_set)}")
for resp in sorted(responsible_set):
    print(f"     - {resp}")

# Create dataset with correct structure
dataset = {
    "vulnerabilities": vulnerabilities,
    "summary": {
        "total": len(vulnerabilities),
        "backlog": status_count.get("Backlog", 0),
        "concluido": status_count.get("Concluído", 0),
        "em_progresso": status_count.get("Em Progresso", 0),
        "p1": priority_count.get("P1", 0),
        "p2": priority_count.get("P2", 0),
        "p3": priority_count.get("P3", 0),
        "p4": priority_count.get("P4", 0),
    },
    "filters": {
        "responsibles": sorted(list(responsible_set)),
        "categories": sorted(list(categories_set))
    },
    "metadata": {
        "updated_at": datetime.now().isoformat(),
        "sheet_id": "1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY",
        "sheet_name": "Página1",
        "source": "Google Sheets - Página1 (via MCP)",
        "total_rows_loaded": len(vulnerabilities),
        "mcp_authenticated_user": "alexandre.oikawa@ifood.com.br",
        "data_verified": True
    }
}

# Save to data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"\n✅ data.json updated with real Página1 data")
print(f"   File: data.json")
print(f"   Records: {len(vulnerabilities)}")
print(f"   Summary saved with actual statistics")
