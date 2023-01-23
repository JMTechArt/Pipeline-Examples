// Fill out your copyright notice in the Description page of Project Settings.


#include "JMBasicScatter.h"
#include "DrawDebugHelpers.h"

// Sets default values
AJMBasicScatter::AJMBasicScatter()
{
	SceneComp = CreateDefaultSubobject<USceneComponent>(TEXT("SceneComp"));
}

void AJMBasicScatter::OnConstruction(const FTransform& Transform)
{
	if (!bDelegatesEnabled)
	{
		GEngine->OnActorMoved().AddUObject(this, &AJMBasicScatter::PostActorMoved);
		GEngine->OnLevelActorAdded().AddUObject(this, &AJMBasicScatter::PostActorAdded);
		GEngine->OnLevelActorDeleted().AddUObject(this, &AJMBasicScatter::PostActorDeleted);
	}	
}

void AJMBasicScatter::PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent)
{

	if (PropertyChangedEvent.ChangeType != EPropertyChangeType::Interactive)
	{
		CreatedPoints.Empty();
		CreatedPoints = CreateGridPoints();
		DisplayGridPoints();
	}

	Super::PostEditChangeProperty(PropertyChangedEvent);
}

void AJMBasicScatter::PostEditMove(bool bFinished)
{
	if (bFinished)
	{
		//UE_LOG(LogTemp, Warning, TEXT("The actor has finished moving."));
	}
	
}

void AJMBasicScatter::PostActorMoved(AActor* Actor)
{
	CreatedPoints.Empty();
	CreatedPoints = CreateGridPoints();
	DisplayGridPoints();
}

void AJMBasicScatter::PostActorAdded(AActor* Actor)
{
	//UE_LOG(LogTemp, Warning, TEXT("Actor was added."));
}

void AJMBasicScatter::PostActorDeleted(AActor* Actor)
{
	//UE_LOG(LogTemp, Warning, TEXT("Actor was deleted."));
}



TArray<FGridPoint> AJMBasicScatter::CreateGridPoints()
{
	TArray<FGridPoint> Points;
	
	if (ScatterSurface)
	{
		FVector Origin, BoxExtent;
		ScatterSurface->GetActorBounds(false, Origin, BoxExtent);

		FVector2D SurfaceLength = FVector2D(BoxExtent.X * 2, BoxExtent.Y * 2);

		for (int x = 0; x <= FMath::FloorToInt(SurfaceLength.X / InstanceSpacing); x++)
		{
			for (int y = 0; y <= FMath::FloorToInt(SurfaceLength.Y / InstanceSpacing); y++)
			{
				float XVal = x * InstanceSpacing;
				float YVal = y * InstanceSpacing;

				FVector PointLocation = FVector
				(
					Origin - FVector(BoxExtent.X, BoxExtent.Y, (BoxExtent.Z * -1.f)) + 
					FVector(XVal, YVal, 0.f)
				);

				FGridPoint NewPoint;
				NewPoint.Location = PointLocation;
				NewPoint.PointColor = FColor::Black;

				Points.Add(NewPoint);
			}
		}
	}

	return Points;
}

void AJMBasicScatter::DisplayGridPoints()
{
	Randomize = FRandomStream(RandomSeed);

	if (CreatedPoints.Num() > 0)
	{
		FlushPersistentDebugLines(GetWorld());

		for (auto Point : CreatedPoints)
		{
			float Size = InstanceSpacing * 0.5f;
			float RandX = Randomize.RandRange(-Size, Size);
			float RandY = Randomize.RandRange(-Size, Size);

			FVector2D RandomPosition = FVector2d(FMath::Sin(RandX) * Size, FMath::Cos(RandY) * Size);
			RandomPosition *= OffsetPercentage;

			FVector Location = Point.Location;
			Location.X += RandomPosition.X;
			Location.Y += RandomPosition.Y;

			DrawDebugPoint(GetWorld(), Location, 20.f, Point.PointColor, true);
		}
	}
}





