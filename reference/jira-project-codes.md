# JIRA Project Codes for TSE Escalations

Last Updated: 2026-02-04
Source: https://datadoghq.atlassian.net/wiki/spaces/TS/pages/348553487

## Support Projects (Escalations)

Format: `Support - {Product}` (PROJECT_KEY)

| Product Area | Project Key | Project Name |
|--------------|-------------|--------------|
| **Agent** | AGENT | Support - Agent |
| **API Management** | SAPIM | Support - API Management |
| **APM** | APMS | Support - APM |
| **Bits AI** | SBA | Support - Bits AI |
| **CI Visibility** | SCV | Support - CI Visibility |
| **CD Visibility** | SCD | Support - CD Visibility |
| **Cloud Cost Management** | SCCM | Support - Cloud Cost Management |
| **Cloud Integrations** | CLOUDS | Support - Cloud Integrations |
| **Cloud Maps** | SCM | Support - Cloud Maps |
| **Code Analysis** | SCODE | Support - Code Analysis |
| **Code Coverage** | SCCOV | Support - Code Coverage |
| **Container Apps** | SCA | Support - Container Apps |
| **Containers** | CONS | Support - Containers |
| **Continuous Profiler** | SCP | Support - Continuous Profiler |
| **CoScreen** | SCOS | Support - CoScreen |
| **Database Monitoring (DBM)** | SDBM | Support - Database Monitoring |
| **Data Stream Monitoring** | DSMS | Support - Data Stream Monitoring |
| **Data Jobs Monitoring** | DJMS | Support - Data Jobs Monitoring |
| **Data Science** | DTSS | Support - Data Science |
| **Datadog Workflows** | DDWF | Support - Datadog Workflows |
| **DORA Metrics** | DORAM | Support - DORA Metrics |
| **Dynamic Instrumentation** | DYNIS | Support - Dynamic Instrumentation |
| **Eppo** | SEPPO | Support - Eppo |
| **Error Tracking** | ERRS | Support - Error Tracking |
| **Fleet Automation** | SPFA | Support - Fleet Automation |
| **GPU Monitoring** | SGPUM | Support - GPU Monitoring |
| **Heroku** | HRKS | Support - Heroku |
| **Internal Developer Portal** | - | Support - Internal Developer Portal |
| **Logs** | LOGSS | Support - Logs |
| **Metrics** | METS | Support - Metrics |
| **ML Observability** | MLOS | Support - ML Observability |
| **Mobile App** | MAPP | Support - Mobile App |
| **Monitors** | MNTS | Support - Monitors |
| **Network Edge** | EDGES | Support - Network Edge |
| **Networks** | NTWK | Support - Networks |
| **Observability Pipelines** | OBPS | Support - Observability Pipelines |
| **Open Telemetry** | OTELS | Support - Open Telemetry |
| **Process Monitoring** | PRMS | Support - Process Monitoring |
| **Remote Config** | RCMS | Support - Remote Config |
| **Revenue Engineering** | SREVENG | Support - Revenue Engineering |
| **RUM** | RUMS | Support - RUM |
| **SaaS Integrations** | - | Support - SaaS Integrations |
| **Security** | SCRS | Support - Security |
| **Serverless** | SLES | Support - Serverless |
| **Service Management** | SOCE | Support - Service Management |
| **Source Code Integration** | SSCI | Support - Source Code Integration |
| **Synthetics** | SYN | Support - Synthetics |
| **Test Visibility** | STV | Support - Test Visibility |
| **Tools and Libraries** | TLIBS | Support - Tools and Libraries |
| **Universal Service Monitoring** | SUSM | Support - Universal Service Monitoring |
| **Web Integrations** | WEBINT | Support - Web Integrations |
| **Web Platform (AAA/Dashboards/Dataviz/Core)** | WEBPS | Support - Web Platform |

## Mapping to TSE Specializations

Based on the TSE spec list you provided:

| TSE Spec | JIRA Project Key | Project Name |
|----------|------------------|--------------|
| **Training Queue** | N/A | (No dedicated escalation project) |
| **Monitors** | MNTS | Support - Monitors |
| **Serverless** | SLES | Support - Serverless |
| **CoScreen** | SCOS | Support - CoScreen |
| **Logs** | LOGSS | Support - Logs |
| **Containers** | CONS | Support - Containers |
| **Metrics** | METS | Support - Metrics |
| **APM** | APMS | Support - APM |
| **Security** | SCRS | Support - Security |
| **DBM** | SDBM | Support - Database Monitoring |
| **Synthetics** | SYN | Support - Synthetics |
| **RUM** | RUMS | Support - RUM |
| **Agent** | AGENT | Support - Agent |
| **Cloud Integrations** | CLOUDS | Support - Cloud Integrations |
| **Misc/New** | *(varies)* | Depends on the product |
| **Web Platform** | WEBPS | Support - Web Platform |
| **Service Management** | SOCE | Support - Service Management |

## Notes

- Each `Support - {Product}` project is for **escalations** to TEE/Engineering
- Feature requests use a different naming: `Support FR - {Product}` (e.g., `FRAPMS` for APM feature requests)
- Some TSE specs may map to multiple JIRA projects depending on the specific issue
- "Misc/New" doesn't have a dedicated project - TSEs should escalate to the most relevant product project

## Related Documentation

- Full Jira Project List: https://datadoghq.atlassian.net/wiki/spaces/TS/pages/348553487
- Escalation Workflow: https://datadoghq.atlassian.net/wiki/spaces/TS/pages/3114041652
- Escalation Template: `/templates/escalation/escalation-template.md`

