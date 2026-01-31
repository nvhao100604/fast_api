class CVSkill(Base):
    __tablename__ = "CVSkills"

    CVId = Column(String(36), ForeignKey("CVs.Id"), primary_key=True)
    SkillId = Column(String(36), ForeignKey("Skills.Id"), primary_key=True)
    Confidence = Column(DECIMAL)
    Source = Column(String(100))

    cv = relationship("CV", back_populates="skills")
